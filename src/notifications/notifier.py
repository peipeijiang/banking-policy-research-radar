"""
通知代理模块 - 多渠道通知系统

支持的通知渠道：
- Email: SMTP 邮件通知
- 企业微信: Webhook 机器人（Markdown 模板）
- 钉钉: Webhook 机器人（支持签名验证）
- Telegram: Bot API
- Slack: Incoming Webhook
- 通用 Webhook: 自定义 URL

支持的通知类型：
- 运行成功/失败通知（基于可自定义模板）
- 错误告警通知（MinerU、LLM、网络、通用错误）
"""

import json
import html
import logging
import os
import re
import smtplib
import hashlib
import hmac
import base64
import time
import urllib.parse
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import List, Dict, Optional, Any

import requests

logger = logging.getLogger(__name__)

# 模板目录
TEMPLATE_DIR = (
    Path(__file__).resolve().parent.parent.parent / "configs" / "templates" / "notifications"
)
EMAIL_TEMPLATE_DIR = (
    Path(__file__).resolve().parent.parent.parent / "configs" / "templates" / "email"
)


def _load_template(name: str, platform: Optional[str] = None) -> Optional[str]:
    """
    加载通知模板文件。

    模板文件存放于 configs/templates/notifications/ 目录，
    以 '# ' 开头（单个 #）的行视为注释，不会出现在最终消息中。
    '## ' 及更多 # 开头的行保留为 Markdown 标题。

    参数:
        name: 模板文件名（不含扩展名），如 'success'、'error_mineru'

    返回:
        去除注释后的模板内容，文件不存在时返回 None
    """
    path = TEMPLATE_DIR / f"{name}.md"

    if not path.exists():
        logger.debug(f"模板文件不存在: {path}")
        return None
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
        content_lines = []
        for line in lines:
            stripped = line.lstrip()
            # 单 # 开头且不是 ## 的行视为注释
            if stripped.startswith("# ") and not stripped.startswith("## "):
                continue
            if stripped == "#":
                continue
            content_lines.append(line)
        return "\n".join(content_lines).strip()
    except Exception as e:
        logger.warning(f"加载模板失败 ({path}): {e}")
        return None


def _render_template(template: str, **kwargs) -> str:
    """渲染模板，将 {变量名} 替换为实际值。未提供的变量保留原样。"""
    result = template
    for key, value in kwargs.items():
        result = result.replace(f"{{{key}}}", str(value))
    return result


def _load_email_template(name: str) -> Optional[str]:
    """
    加载 HTML 邮件通知模板文件。

    模板文件存放于 configs/templates/email/ 目录，以 .html 为扩展名。
    HTML 文件开头的 HTML 注释（<!-- ... -->）会被保留，不做处理。

    参数:
        name: 模板文件名（不含扩展名），如 'success'、'error_llm'

    返回:
        模板 HTML 内容，文件不存在时返回 None
    """
    path = EMAIL_TEMPLATE_DIR / f"{name}.html"
    if not path.exists():
        logger.debug(f"HTML 邮件模板不存在: {path}")
        return None
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        logger.warning(f"加载 HTML 邮件模板失败 ({path}): {e}")
        return None


@dataclass
class RunResult:
    """管道运行结果摘要"""

    run_timestamp: str = ""
    total_papers_fetched: int = 0
    papers_by_source: Dict[str, int] = field(default_factory=dict)
    qualified_by_source: Dict[str, int] = field(default_factory=dict)
    analyzed_by_source: Dict[str, int] = field(default_factory=dict)
    report_paths: Dict[str, str] = field(default_factory=dict)
    total_qualified: int = 0
    total_analyzed: int = 0
    success: bool = True
    error_message: Optional[str] = None
    top_papers: List[Dict[str, Any]] = field(default_factory=list)
    token_usage: Dict[str, Any] = field(default_factory=dict)
    summary_mode: str = "run"
    summary_label: str = ""


@dataclass
class TrendRunResult:
    """研究趋势分析运行结果摘要"""

    run_timestamp: str = ""
    keywords: List[str] = field(default_factory=list)
    date_from: str = ""
    date_to: str = ""
    total_papers: int = 0
    tldr_count: int = 0
    trend_skills_count: int = 0
    report_paths: Dict[str, str] = field(default_factory=dict)
    success: bool = True
    error_message: Optional[str] = None
    token_usage: Dict[str, Any] = field(default_factory=dict)


class BaseNotifier(ABC):
    """通知器抽象基类"""

    @abstractmethod
    def send(self, subject: str, body: str, attachments: Optional[List[Path]] = None) -> bool:
        """发送通知，成功返回 True"""
        ...


class EmailNotifier(BaseNotifier):
    """SMTP 邮件通知"""

    def __init__(
        self,
        host: str,
        port: int,
        user: str,
        password: str,
        from_addr: str,
        to_addrs: List[str],
        use_tls: bool = True,
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.from_addr = from_addr or user
        self.to_addrs = to_addrs
        self.use_tls = use_tls

    def send(
        self,
        subject: str,
        body: str,
        attachments: Optional[List[Path]] = None,
        html_body: Optional[str] = None,
    ) -> bool:
        # 根据是否有附件和 HTML 选择合适的 MIME 结构
        if attachments:
            # 有附件：外层 mixed，内层 alternative（如有 HTML）
            msg = MIMEMultipart("mixed")
            msg["From"] = self.from_addr
            msg["To"] = ", ".join(self.to_addrs)
            msg["Subject"] = subject
            if html_body:
                alt_part = MIMEMultipart("alternative")
                alt_part.attach(MIMEText(body, "plain", "utf-8"))
                alt_part.attach(MIMEText(html_body, "html", "utf-8"))
                msg.attach(alt_part)
            else:
                msg.attach(MIMEText(body, "plain", "utf-8"))
        elif html_body:
            # 无附件 + HTML：直接用 alternative
            msg = MIMEMultipart("alternative")
            msg["From"] = self.from_addr
            msg["To"] = ", ".join(self.to_addrs)
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain", "utf-8"))
            msg.attach(MIMEText(html_body, "html", "utf-8"))
        else:
            # 仅纯文本
            msg = MIMEMultipart()
            msg["From"] = self.from_addr
            msg["To"] = ", ".join(self.to_addrs)
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain", "utf-8"))

        # 附件
        if attachments:
            for filepath in attachments:
                if filepath.exists() and filepath.is_file():
                    part = MIMEBase("application", "octet-stream")
                    with open(filepath, "rb") as f:
                        part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename={filepath.name}")
                    msg.attach(part)

        # 发送
        if self.port == 465:
            # SSL 直连
            with smtplib.SMTP_SSL(self.host, self.port, timeout=30) as server:
                server.login(self.user, self.password)
                server.sendmail(self.from_addr, self.to_addrs, msg.as_string())
        else:
            # STARTTLS
            with smtplib.SMTP(self.host, self.port, timeout=30) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.user, self.password)
                server.sendmail(self.from_addr, self.to_addrs, msg.as_string())

        logger.info(f"邮件已发送至: {', '.join(self.to_addrs)}")
        return True


class WebhookNotifier(BaseNotifier):
    """多平台 Webhook 通知"""

    def __init__(self, platform: str, webhook_url: str, **kwargs):
        self.platform = platform
        self.webhook_url = webhook_url
        self.extra = kwargs  # secret, chat_id 等

    def send(self, subject: str, body: str, attachments: Optional[List[Path]] = None) -> bool:
        formatter = getattr(self, f"_format_{self.platform}", self._format_generic)
        url, payload, headers = formatter(subject, body)
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()

        # These APIs can report application errors in an HTTP 200 response.
        if self.platform in {"wechat_work", "dingtalk", "telegram"}:
            try:
                response_data = resp.json()
            except ValueError as exc:
                raise RuntimeError(
                    f"Webhook [{self.platform}] returned invalid JSON"
                ) from exc

            if self.platform == "telegram":
                if response_data.get("ok") is not True:
                    description = response_data.get("description", "unknown error")
                    raise RuntimeError(f"Webhook [telegram] rejected message: {description}")
            elif response_data.get("errcode", 0) != 0:
                errcode = response_data.get("errcode")
                errmsg = response_data.get("errmsg", "unknown error")
                raise RuntimeError(
                    f"Webhook [{self.platform}] rejected message: {errcode} {errmsg}"
                )

        logger.info(f"Webhook [{self.platform}] 通知已发送")
        return True

    def _format_wechat_work(self, subject: str, body: str):
        """企业微信机器人 — body 已含完整 Markdown 模板内容"""
        content = self._truncate_wechat_markdown(body)
        payload = {"msgtype": "markdown", "markdown": {"content": content}}
        return self.webhook_url, payload, {"Content-Type": "application/json"}

    @staticmethod
    def _truncate_wechat_markdown(content: str, max_bytes: int = 4000) -> str:
        """Truncate only at line boundaries so Markdown links are never cut open."""
        if len(content.encode("utf-8")) <= max_bytes:
            return content
        marker = "\n\n...(更多论文请查看完整报告)"
        budget = max_bytes - len(marker.encode("utf-8"))
        kept = []
        used = 0
        for line in content.splitlines(keepends=True):
            size = len(line.encode("utf-8"))
            if used + size > budget:
                break
            kept.append(line)
            used += size
        return "".join(kept).rstrip() + marker

    def _format_dingtalk(self, subject: str, body: str):
        """钉钉机器人（支持签名验证）"""
        url = self.webhook_url
        secret = self.extra.get("secret", "")
        if secret:
            timestamp = str(round(time.time() * 1000))
            string_to_sign = f"{timestamp}\n{secret}"
            hmac_code = hmac.new(
                secret.encode("utf-8"), string_to_sign.encode("utf-8"), digestmod=hashlib.sha256
            ).digest()
            sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
            url = f"{url}&timestamp={timestamp}&sign={sign}"

        payload = {"msgtype": "markdown", "markdown": {"title": subject, "text": body}}
        return url, payload, {"Content-Type": "application/json"}

    def _format_telegram(self, subject: str, body: str):
        """Telegram Bot"""
        chat_id = self.extra.get("chat_id", "")
        text = f"<b>{html.escape(subject)}</b>\n\n{body}"
        # Telegram 消息限 4096 字符
        if len(text) > 4000:
            text = text[:3900] + "\n\n...(内容已截断)"
        payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
        return self.webhook_url, payload, {"Content-Type": "application/json"}

    def _format_slack(self, subject: str, body: str):
        """Slack Incoming Webhook"""
        payload = {
            "blocks": [
                {"type": "header", "text": {"type": "plain_text", "text": subject}},
                {"type": "section", "text": {"type": "mrkdwn", "text": body}},
            ]
        }
        return self.webhook_url, payload, {"Content-Type": "application/json"}

    def _format_generic(self, subject: str, body: str):
        """通用 Webhook"""
        payload = {"subject": subject, "body": body, "timestamp": datetime.now().isoformat()}
        return self.webhook_url, payload, {"Content-Type": "application/json"}


class NotifierAgent:
    """通知编排代理，管理所有已配置的通知渠道"""

    def __init__(self):
        from config import settings

        self.settings = settings
        self.notifiers: List[BaseNotifier] = []
        self._setup_notifiers()

    def _setup_notifiers(self):
        """根据配置初始化通知渠道"""
        s = self.settings

        # Email
        if s.NOTIFY_EMAIL_ENABLED and s.SMTP_HOST and s.SMTP_TO:
            to_addrs = [a.strip() for a in s.SMTP_TO.split(",") if a.strip()]
            self.notifiers.append(
                EmailNotifier(
                    host=s.SMTP_HOST,
                    port=s.SMTP_PORT,
                    user=s.SMTP_USER,
                    password=s.SMTP_PASSWORD,
                    from_addr=s.SMTP_FROM,
                    to_addrs=to_addrs,
                    use_tls=s.SMTP_USE_TLS,
                )
            )
            logger.info("已启用邮件通知")

        # 企业微信
        if s.NOTIFY_WECHAT_ENABLED and s.WECHAT_WEBHOOK_URL:
            self.notifiers.append(WebhookNotifier("wechat_work", s.WECHAT_WEBHOOK_URL))
            logger.info("已启用企业微信通知")

        # 钉钉
        if s.NOTIFY_DINGTALK_ENABLED and s.DINGTALK_WEBHOOK_URL:
            self.notifiers.append(
                WebhookNotifier("dingtalk", s.DINGTALK_WEBHOOK_URL, secret=s.DINGTALK_SECRET)
            )
            logger.info("已启用钉钉通知")

        # Telegram
        if s.NOTIFY_TELEGRAM_ENABLED and s.TELEGRAM_BOT_TOKEN and s.TELEGRAM_CHAT_ID:
            url = f"https://api.telegram.org/bot{s.TELEGRAM_BOT_TOKEN}/sendMessage"
            self.notifiers.append(WebhookNotifier("telegram", url, chat_id=s.TELEGRAM_CHAT_ID))
            logger.info("已启用 Telegram 通知")

        # Slack
        if s.NOTIFY_SLACK_ENABLED and s.SLACK_WEBHOOK_URL:
            self.notifiers.append(WebhookNotifier("slack", s.SLACK_WEBHOOK_URL))
            logger.info("已启用 Slack 通知")

        # 通用 Webhook
        if s.NOTIFY_GENERIC_WEBHOOK_ENABLED and s.GENERIC_WEBHOOK_URL:
            self.notifiers.append(WebhookNotifier("generic", s.GENERIC_WEBHOOK_URL))
            logger.info("已启用通用 Webhook 通知")

    # ------------------------------------------------------------------
    # 运行结果通知
    # ------------------------------------------------------------------

    @staticmethod
    def _feedback_links(paper: Dict[str, Any]) -> str:
        repo_url = os.getenv("FEEDBACK_REPO_URL", "").rstrip("/")
        api_url = os.getenv("FEEDBACK_API_URL", "").rstrip("/")
        signing_secret = os.getenv("FEEDBACK_SIGNING_SECRET", "")
        paper_id = paper.get("paper_id", "")
        if not paper_id:
            return ""
        links = []
        for action, label in (("LIKE", "喜欢"), ("IGNORE", "忽略")):
            if api_url and signing_secret:
                message = f"{action}\n{paper_id}".encode("utf-8")
                signature = hmac.new(
                    signing_secret.encode("utf-8"), message, hashlib.sha256
                ).hexdigest()
                query = urllib.parse.urlencode(
                    {"action": action, "paper_id": paper_id, "sig": signature}
                )
                links.append(f"[{label}]({api_url}/feedback?{query})")
            elif repo_url:
                query = urllib.parse.urlencode(
                    {"labels": "paper-feedback", "title": f"[{action}] {paper_id}"}
                )
                links.append(f"[{label}]({repo_url}/issues/new?{query})")
        return " | ".join(links)

    def notify(self, result: RunResult) -> bool:
        """格式化并发送运行结果通知，全部成功时返回 True。"""
        if not self.notifiers:
            logger.error("未配置任何通知渠道，无法发送")
            return False

        if result.success and not self.settings.NOTIFY_ON_SUCCESS:
            return True
        if not result.success and not self.settings.NOTIFY_ON_FAILURE:
            return True

        subject = self._format_subject(result)
        html_body = self._format_html_body(result)
        attachments = (
            self._collect_attachments(result) if self.settings.NOTIFY_ATTACH_REPORTS else []
        )

        delivery_succeeded = True
        for notifier in self.notifiers:
            try:
                platform = self._platform_for_notifier(notifier)
                if platform in {"wechat_work", "dingtalk"} and result.success:
                    if platform == "dingtalk":
                        overview = self._format_dingtalk_overview(result)
                        format_cards = self._format_dingtalk_paper_cards
                    else:
                        overview = self._format_wechat_overview(result)
                        format_cards = self._format_wechat_paper_cards
                    notifier.send(subject, overview, attachments)
                    for index, paper in enumerate(result.top_papers, 1):
                        try:
                            for card in format_cards(paper, index, len(result.top_papers)):
                                notifier.send(subject, card)
                                time.sleep(0.35)
                        except Exception as exc:
                            delivery_succeeded = False
                            logger.error(
                                f"{platform} 论文卡片发送失败 ({paper.get('paper_id')}): {exc}"
                            )
                    continue
                body = self._format_body_for_platform(result, platform)
                if isinstance(notifier, EmailNotifier) and html_body:
                    notifier.send(subject, body, attachments, html_body=html_body)
                else:
                    notifier.send(subject, body, attachments)
            except Exception as e:
                delivery_succeeded = False
                logger.error(f"通知发送失败 ({type(notifier).__name__}): {e}")

        return delivery_succeeded

    @staticmethod
    def _brief(value: Any, limit: int) -> str:
        if isinstance(value, list):
            value = value[0] if value else ""
        value = " ".join(str(value or "").split())
        return value[:limit] + ("…" if len(value) > limit else "")

    @staticmethod
    def _analysis_text(value: Any) -> str:
        if isinstance(value, dict):
            labels = {
                "paper_limitations": "论文本身局限",
                "evidence_limitations": "当前证据局限",
            }
            parts = []
            for key, item in value.items():
                text = NotifierAgent._analysis_text(item)
                if text:
                    label = labels.get(key, str(key).replace("_", " "))
                    parts.append(f"{label}：{text.rstrip('；。')}")
            return "；".join(parts)
        if isinstance(value, list):
            return "；".join(
                NotifierAgent._analysis_text(item) for item in value if item
            )
        return " ".join(str(value or "").split())

    @staticmethod
    def _publication_metadata(paper: Dict[str, Any]) -> tuple[str, str, str, str]:
        source = str(paper.get("source") or "").strip().lower()
        venue = NotifierAgent._analysis_text(paper.get("journal"))
        if not venue:
            venue = {
                "arxiv": "arXiv 预印本",
                "openreview": "OpenReview 公开论文",
                "repec": "RePEc 工作论文系列",
                "worldbank": "World Bank Policy Research Working Papers",
                "bis": "Bank for International Settlements",
            }.get(source, "未识别具体刊物")
        publication_type = str(paper.get("publication_type") or "").strip().lower()
        type_label = {
            "proceedings-article": "会议论文",
            "journal-article": "期刊论文",
            "article": "论文",
            "preprint": "预印本",
            "posted-content": "预印本",
            "working-paper": "工作论文",
            "report": "研究报告",
            "edited-book": "学术专著",
            "book": "学术专著",
            "monograph": "学术专著",
            "book-chapter": "书籍章节",
        }.get(publication_type, "论文")
        published = paper.get("published_date")
        if hasattr(published, "isoformat"):
            published = published.isoformat()
        date_label = str(published or "").split("T", 1)[0] or "日期未标注"
        return venue, type_label, date_label, source.upper() or "未标注"

    @staticmethod
    def _split_text_by_bytes(text: str, max_bytes: int = 2400) -> List[str]:
        chunks, current, size = [], [], 0
        for char in text:
            char_size = len(char.encode("utf-8"))
            if current and size + char_size > max_bytes:
                chunks.append("".join(current))
                current, size = [], 0
            current.append(char)
            size += char_size
        if current:
            chunks.append("".join(current))
        return chunks or [""]

    def _format_wechat_overview(self, result: RunResult) -> str:
        field_name = getattr(
            getattr(self, "settings", None), "RESEARCH_FIELD_NAME", "推荐系统"
        )
        source_lines = []
        for source in sorted(result.papers_by_source):
            if result.summary_mode == "curated":
                source_lines.append(
                    f"> `{source.upper()}` 精选 **{result.papers_by_source[source]}** | "
                    f"全文 **{result.analyzed_by_source.get(source, 0)}**"
                )
            else:
                source_lines.append(
                    f"> `{source.upper()}` 抓取 **{result.papers_by_source[source]}** | "
                    f"及格 **{result.qualified_by_source.get(source, 0)}** | "
                    f"分析 **{result.analyzed_by_source.get(source, 0)}**"
                )
        token_line = ""
        total_tokens = (result.token_usage or {}).get("total")
        if total_tokens:
            token_line = f"\n> Token：{total_tokens:,}"
        full_text_count = sum(
            1
            for paper in result.top_papers
            if (paper.get("analysis") or {}).get("_analysis_basis") == "full_text"
        )
        abstract_only_count = len(result.top_papers) - full_text_count
        basis_line = ""
        if result.top_papers:
            basis_line = (
                f"\n> 全文深读 **{full_text_count}** 篇 · "
                f"仅摘要 **{abstract_only_count}** 篇"
            )
            if abstract_only_count:
                basis_line += (
                    "\n<font color=\"warning\">存在未获取正文的论文，"
                    "对应卡片已标记证据限制。</font>"
                )
        if result.summary_mode == "curated":
            summary_line = (
                f"> {result.summary_label or '全文精选'} **{len(result.top_papers)}** 篇 · "
                f"全文深读 **{full_text_count}** 篇"
            )
        else:
            summary_line = (
                f"> 抓取 **{result.total_papers_fetched}** 篇 · "
                f"及格 **{result.total_qualified}** 篇 · "
                f"深度分析 **{result.total_analyzed}** 篇{token_line}{basis_line}"
            )
        return (
            f"## {field_name}每日研究\n"
            f"<font color=\"info\">运行成功</font> · {result.run_timestamp}\n\n"
            f"{summary_line}\n\n"
            + "\n".join(source_lines)
            + f"\n\n随后发送 Top {len(result.top_papers)} 单篇研究卡片。"
        )

    @staticmethod
    def _as_dingtalk_markdown(content: str) -> str:
        """Remove WeCom-only color tags while preserving Markdown links."""
        return re.sub(r"</?font(?:\s+[^>]*)?>", "", content, flags=re.I)

    def _format_dingtalk_overview(self, result: RunResult) -> str:
        return self._as_dingtalk_markdown(self._format_wechat_overview(result))

    def _format_dingtalk_paper_cards(
        self, paper: Dict[str, Any], index: int, total: int
    ) -> List[str]:
        return [
            self._as_dingtalk_markdown(card)
            for card in self._format_wechat_paper_cards(paper, index, total)
        ]

    def _format_wechat_paper_card(
        self, paper: Dict[str, Any], index: int, total: int
    ) -> str:
        """Backward-compatible single-card accessor; notification uses all returned parts."""
        return self._format_wechat_paper_cards(paper, index, total)[0]

    def _format_wechat_paper_cards(
        self, paper: Dict[str, Any], index: int, total: int
    ) -> List[str]:
        analysis = paper.get("analysis") or {}
        basis = analysis.get("_analysis_basis")
        if basis == "full_text":
            level = "全文深读"
            basis_warning = ""
        elif basis == "abstract":
            level = "摘要分析"
            basis_warning = (
                '<font color="warning">未获取论文正文，本卡片仅基于摘要；'
                "实验细节、关键结果和局限性可能不完整。</font>"
            )
        else:
            level = "摘要速览" if not analysis else "深度分析"
            basis_warning = (
                '<font color="warning">未确认获取论文正文，本卡片基于有限材料；'
                "请谨慎使用实验结论和局限性分析。</font>"
            )

        title = analysis.get("chinese_title") or paper.get("title", "")
        original_title = paper.get("title", "")
        summary = self._analysis_text(analysis.get("summary") or paper.get("tldr"))
        methodology = self._analysis_text(analysis.get("methodology"))
        results = self._analysis_text(analysis.get("key_results"))
        limitations = self._analysis_text(analysis.get("limitations"))

        sections = [("核心结论", summary)]
        personalization = paper.get("personalization") or {}
        if personalization.get("active"):
            mode_label = "影子评分" if personalization.get("mode") == "shadow" else "个性化评分"
            reasons = "；".join(personalization.get("reasons") or [])
            sections.append(
                (
                    "推荐理由",
                    f"{mode_label} {personalization.get('personalized_score', paper.get('score', 0)):.1f} "
                    f"（调整 {personalization.get('adjustment', 0):+.1f}）"
                    + (f"；{reasons}" if reasons else "")
                    + ("；探索位" if personalization.get("exploration") else ""),
                )
            )
        if methodology:
            sections.append(("方法", methodology))
        if results:
            sections.append(("关键结果", results))
        if limitations:
            sections.append(("主要局限", limitations))

        repositories = paper.get("code_repositories") or []
        if repositories:
            repo = repositories[0]
            sections.append(
                (
                    "代码",
                    f"[{repo.get('full_name')}]({repo.get('url')}) · "
                    f"{repo.get('classification')} · 置信度 {repo.get('confidence')}",
                )
            )
        elif analysis:
            sections.append(("代码", "尚未发现可信的论文实现仓库"))

        repo_url = os.getenv("FEEDBACK_REPO_URL", "").rstrip("/")
        paper_id = paper.get("paper_id", "")
        slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", paper_id).strip("-")[:140]
        report_link = (
            f"[深度报告]({repo_url}/blob/main/knowledge/papers/{slug}.md)" if repo_url else ""
        )
        original_link = f"[查看原文]({paper.get('url')})" if paper.get("url") else ""
        links = " · ".join(link for link in (report_link, original_link) if link)
        feedback = self._feedback_links(paper)
        venue, publication_type, published_date, discovery_source = self._publication_metadata(paper)
        domain_scores = paper.get("domain_scores") or {}
        domain_labels = {
            "commercial_banking": "商业银行",
            "monetary_policy": "货币政策",
            "fiscal_policy": "财政政策",
        }
        domain_line = ""
        if domain_scores:
            matched_label = paper.get("matched_domain_label") or domain_labels.get(
                paper.get("matched_domain"), paper.get("matched_domain", "")
            )
            score_parts = [
                f"{domain_labels.get(key, key)} {float(value):.1f}"
                for key, value in domain_scores.items()
            ]
            domain_line = (
                f"\n<font color=\"info\">命中领域：{matched_label}</font> · "
                + " / ".join(score_parts)
            )
        base_header = f"## {index}/{total} · {title}\n"
        if title != original_title:
            base_header += f"> {original_title}\n\n"
        else:
            base_header += "\n"
        base_header += (
            f"**期刊 / 会议 / 系列**\n> {venue}\n\n"
            f"`{publication_type}` · `{published_date}`\n"
            f"<font color=\"{'info' if basis == 'full_text' else 'warning'}\">{level}</font> · "
            f"基础分 **{paper.get('score', 0):.1f}**\n"
            f"<font color=\"comment\">发现渠道：{discovery_source}</font>"
            f"{domain_line}"
        )
        if basis_warning:
            base_header += f"\n\n> **证据限制**：{basis_warning}"
        blocks = []
        for label, value in sections:
            chunks = self._split_text_by_bytes(value)
            for chunk_index, chunk in enumerate(chunks):
                suffix = "（续）" if chunk_index else ""
                blocks.append(f"**{label}{suffix}**\n> {chunk}")
        footer = "\n\n".join(value for value in (links, feedback) if value)
        if footer:
            blocks.append(footer)

        pages, current = [], []
        for block in blocks:
            candidate = base_header + "\n\n" + "\n\n".join(current + [block])
            if current and len(candidate.encode("utf-8")) > 3650:
                pages.append(current)
                current = [block]
            else:
                current.append(block)
        if current:
            pages.append(current)

        rendered = []
        page_total = len(pages)
        for page_index, page_blocks in enumerate(pages, 1):
            part = f" · {page_index}/{page_total}" if page_total > 1 else ""
            header = base_header.replace(
                f"## {index}/{total} ·", f"## {index}/{total}{part} ·", 1
            )
            content = header + "\n\n" + "\n\n".join(page_blocks)
            rendered.append(WebhookNotifier._truncate_wechat_markdown(content))
        return rendered

    # ------------------------------------------------------------------
    # 研究趋势分析结果通知
    # ------------------------------------------------------------------

    def notify_trend(self, result: TrendRunResult) -> None:
        """格式化并发送研究趋势分析结果通知到所有已配置的渠道"""
        if not self.notifiers:
            logger.debug("未配置任何通知渠道，跳过")
            return

        if result.success and not self.settings.NOTIFY_ON_SUCCESS:
            return
        if not result.success and not self.settings.NOTIFY_ON_FAILURE:
            return

        subject = self._format_trend_subject(result)
        html_body = self._format_trend_html_body(result)
        attachments = (
            self._collect_trend_attachments(result) if self.settings.NOTIFY_ATTACH_REPORTS else []
        )

        for notifier in self.notifiers:
            try:
                platform = self._platform_for_notifier(notifier)
                body = self._format_trend_body_for_platform(result, platform)
                if isinstance(notifier, EmailNotifier) and html_body:
                    notifier.send(subject, body, attachments, html_body=html_body)
                else:
                    notifier.send(subject, body, attachments)
            except Exception as e:
                logger.warning(f"趋势通知发送失败 ({type(notifier).__name__}): {e}")

    # ------------------------------------------------------------------
    # 错误告警通知
    # ------------------------------------------------------------------

    def notify_error(self, template_name: str, **kwargs) -> None:
        """
        发送错误告警通知。

        使用 configs/templates/notifications/ 下的错误模板文件渲染消息并发送。
        仅在 on_failure 为 True 时发送。模板或渠道不存在时静默跳过。

        参数:
            template_name: 模板名称（如 'error_mineru'、'error_llm'、'error_network'、'error_generic'）
            **kwargs: 模板变量
        """
        if not self.notifiers:
            return
        if not self.settings.NOTIFY_ON_FAILURE:
            return

        if "timestamp" not in kwargs:
            kwargs["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        subject = f"ArXiv Daily Researcher - ERROR ({kwargs.get('timestamp', '')})"

        for notifier in self.notifiers:
            try:
                platform = self._platform_for_notifier(notifier)
                body = self._format_error_body_for_platform(template_name, platform, **kwargs)
                if isinstance(notifier, EmailNotifier):
                    html_body = self._format_html_error_body(template_name, **kwargs)
                    notifier.send(subject, body, html_body=html_body)
                else:
                    notifier.send(subject, body)
            except Exception as e:
                logger.warning(f"错误告警发送失败 ({type(notifier).__name__}): {e}")

    # ------------------------------------------------------------------
    # 格式化辅助方法
    # ------------------------------------------------------------------

    def _format_token_section_md(self, token_usage: Dict[str, Any]) -> str:
        """格式化 token 消耗为 Markdown 片段（tracking 未开启或无数据返回空字符串）"""
        if not self.settings.TOKEN_TRACKING_ENABLED:
            return ""
        if not token_usage or not token_usage.get("has_data"):
            return ""
        total = token_usage.get("total", 0)
        tp = token_usage.get("total_prompt", 0)
        tc = token_usage.get("total_completion", 0)
        return f"> Token 消耗: **{total:,}** tokens（输入 {tp:,} / 输出 {tc:,}）"

    def _format_token_section_html(self, token_usage: Dict[str, Any]) -> str:
        """格式化 token 消耗为 HTML 行片段（tracking 未开启或无数据返回空字符串）"""
        if not self.settings.TOKEN_TRACKING_ENABLED:
            return ""
        if not token_usage or not token_usage.get("has_data"):
            return ""
        total = token_usage.get("total", 0)
        tp = token_usage.get("total_prompt", 0)
        tc = token_usage.get("total_completion", 0)
        return (
            f'<tr><td style="padding:4px 32px 16px;">'
            f'<p style="margin:0;font-size:12px;color:#9ca3af;">'
            f'Token 消耗: <strong style="color:#6b7280;">{total:,}</strong> tokens'
            f'（输入 {tp:,} / 输出 {tc:,}）</p></td></tr>'
        )

    def _format_subject(self, result: RunResult) -> str:
        status = "SUCCESS" if result.success else "FAILED"
        return f"ArXiv Daily Researcher - {status} ({result.run_timestamp})"

    def _format_body(self, result: RunResult) -> str:
        """向后兼容：默认使用通用模板（非 Telegram 专用）"""
        template_name = "success" if result.success else "failure"
        template = _load_template(template_name)

        # 构建各数据源统计文本
        source_lines = []
        for source in sorted(result.papers_by_source.keys()):
            fetched = result.papers_by_source.get(source, 0)
            qualified = result.qualified_by_source.get(source, 0)
            analyzed = result.analyzed_by_source.get(source, 0)
            source_lines.append(
                f"> `{source.upper()}` 抓取 **{fetched}** | 及格 **{qualified}** | 分析 **{analyzed}**"
            )
        source_summary = "\n".join(source_lines)

        # 构建报告路径文本
        report_lines = []
        if result.report_paths:
            report_lines.append("**报告路径**")
            for source, path in result.report_paths.items():
                report_lines.append(f"> `{source}` {path}")
        report_list = "\n".join(report_lines)

        # 构建 Top-N 论文文本
        top_lines = []
        if result.top_papers:
            top_lines.append(f"**Top {len(result.top_papers)} 论文**")
            for i, p in enumerate(result.top_papers, 1):
                title = p.get("title", "")[:60]
                score = p.get("score", 0)
                src = p.get("source", "").upper()
                tldr = p.get("tldr", "")[:80]
                url = p.get("url", "")
                top_lines.append(f"> **{i}.** `{src}` {title}")
                top_lines.append(f'> <font color="comment">Score: {score:.1f} | {tldr}</font>')
                if url:
                    top_lines.append(f"> [查看原文]({url})")
                feedback = self._feedback_links(p)
                if feedback:
                    top_lines.append(f"> {feedback}")
        top_papers = "\n".join(top_lines)

        if template:
            return _render_template(
                template,
                status="SUCCESS" if result.success else "FAILED",
                timestamp=result.run_timestamp,
                total_fetched=result.total_papers_fetched,
                total_qualified=result.total_qualified,
                total_analyzed=result.total_analyzed,
                source_summary=source_summary,
                report_list=report_list,
                top_papers=top_papers,
                error_message=result.error_message or "无",
                token_usage_section=self._format_token_section_md(result.token_usage),
            )

        # 模板不存在时降级为纯文本
        return self._format_body_fallback(result)

    def _format_body_for_platform(self, result: RunResult, platform: Optional[str]) -> str:
        """使用模板格式化运行结果通知正文，模板不存在时降级为纯文本"""
        if platform == "telegram":
            return self._format_telegram_body(result)

        template_name = "success" if result.success else "failure"
        template = _load_template(template_name)

        # 构建各数据源统计文本
        source_lines = []
        for source in sorted(result.papers_by_source.keys()):
            fetched = result.papers_by_source.get(source, 0)
            qualified = result.qualified_by_source.get(source, 0)
            analyzed = result.analyzed_by_source.get(source, 0)
            source_lines.append(
                f"> `{source.upper()}` 抓取 **{fetched}** | 及格 **{qualified}** | 分析 **{analyzed}**"
            )
        source_summary = "\n".join(source_lines)

        # 构建报告路径文本
        report_lines = []
        if result.report_paths:
            report_lines.append("**报告路径**")
            for source, path in result.report_paths.items():
                report_lines.append(f"> `{source}` {path}")
        report_list = "\n".join(report_lines)

        # 构建 Top-N 论文文本
        top_lines = []
        if result.top_papers:
            top_lines.append(f"**Top {len(result.top_papers)} 论文**")
            for i, p in enumerate(result.top_papers, 1):
                title = p.get("title", "")[:60]
                score = p.get("score", 0)
                src = p.get("source", "").upper()
                tldr = p.get("tldr", "")[:80]
                url = p.get("url", "")
                top_lines.append(f"> **{i}.** `{src}` {title}")
                top_lines.append(f'> <font color="comment">Score: {score:.1f} | {tldr}</font>')
                if url:
                    top_lines.append(f"> [查看原文]({url})")
                feedback = self._feedback_links(p)
                if feedback:
                    top_lines.append(f"> {feedback}")
        top_papers = "\n".join(top_lines)

        if template:
            return _render_template(
                template,
                status="SUCCESS" if result.success else "FAILED",
                timestamp=result.run_timestamp,
                total_fetched=result.total_papers_fetched,
                total_qualified=result.total_qualified,
                total_analyzed=result.total_analyzed,
                source_summary=source_summary,
                report_list=report_list,
                top_papers=top_papers,
                error_message=result.error_message or "无",
                token_usage_section=self._format_token_section_md(result.token_usage),
            )

        # 模板不存在时降级为纯文本
        return self._format_body_fallback(result)

    def _format_telegram_body(self, result: RunResult) -> str:
        """Telegram 专用 HTML 正文，使用 Bot API 支持的实体标签。"""
        status_label = "运行成功" if result.success else "运行失败"
        source_lines = []
        for source in sorted(result.papers_by_source.keys()):
            fetched = result.papers_by_source.get(source, 0)
            qualified = result.qualified_by_source.get(source, 0)
            analyzed = result.analyzed_by_source.get(source, 0)
            source_lines.append(
                f"<code>{self._html_escape(source.upper())}</code> 抓取 <b>{fetched}</b> | 及格 <b>{qualified}</b> | 分析 <b>{analyzed}</b>"
            )

        top_cards = []
        if result.top_papers:
            for i, paper in enumerate(result.top_papers, 1):
                title = self._html_escape(paper.get("title", "")[:80])
                score = paper.get("score", 0)
                src = self._html_escape(paper.get("source", "").upper())
                tldr = self._html_escape(paper.get("tldr", "")[:140])
                url = self._html_escape(paper.get("url", ""))
                card_lines = [
                    f"<b>{i}. <code>{src}</code> {title}</b>",
                    f"<blockquote>Score: <b>{score:.1f}</b>",
                    f"{tldr}</blockquote>",
                ]
                if url:
                    card_lines.append(f'<a href="{url}">查看原文</a>')
                top_cards.append("\n".join(card_lines))

        report_lines = []
        for source, path in sorted(result.report_paths.items()):
            report_lines.append(f"<code>{self._html_escape(source)}</code> {self._html_escape(path)}")

        sections = [
            "<b>ArXiv Daily Researcher</b>",
            f"<b>{status_label}</b> | {self._html_escape(result.run_timestamp)}",
            "",
            "<b>本次运行统计</b>",
            "\n".join(source_lines) if source_lines else "暂无数据",
        ]

        if result.token_usage and result.token_usage.get("has_data") and self.settings.TOKEN_TRACKING_ENABLED:
            total = result.token_usage.get("total", 0)
            tp = result.token_usage.get("total_prompt", 0)
            tc = result.token_usage.get("total_completion", 0)
            sections.extend(
                [
                    "<b>Token 消耗</b>",
                    (
                        f"<blockquote>总计 <b>{total:,}</b> tokens"
                        f"（输入 {tp:,} / 输出 {tc:,}）</blockquote>"
                    ),
                ]
            )

        if top_cards:
            sections.extend(["<b>Top 论文</b>", *top_cards])

        if report_lines:
            sections.extend(["<b>报告路径</b>", "\n".join(report_lines)])

        if not result.success and result.error_message:
            sections.extend(["<b>错误信息</b>", f"<blockquote>{self._html_escape(result.error_message)}</blockquote>"])

        return "\n".join(sections)

    def _format_body_fallback(self, result: RunResult) -> str:
        """模板不存在时的兜底纯文本格式（保持向后兼容）"""
        status_icon = "OK" if result.success else "ERROR"
        lines = [
            f"Status: {status_icon}",
            f"Time: {result.run_timestamp}",
            "",
        ]

        if result.error_message:
            lines.append(f"Error: {result.error_message}")
            lines.append("")

        lines.append("Papers Summary:")
        for source in sorted(result.papers_by_source.keys()):
            fetched = result.papers_by_source.get(source, 0)
            qualified = result.qualified_by_source.get(source, 0)
            analyzed = result.analyzed_by_source.get(source, 0)
            lines.append(
                f"  [{source.upper()}] Fetched: {fetched} | Qualified: {qualified} | Analyzed: {analyzed}"
            )

        lines.append("")
        lines.append(
            f"Total: Fetched {result.total_papers_fetched} | "
            f"Qualified {result.total_qualified} | "
            f"Analyzed {result.total_analyzed}"
        )

        if result.report_paths:
            lines.append("")
            lines.append("Reports:")
            for source, path in result.report_paths.items():
                lines.append(f"  [{source}] {path}")

        if result.top_papers:
            lines.append("")
            lines.append(f"Top {len(result.top_papers)} Papers:")
            for i, p in enumerate(result.top_papers, 1):
                title = p.get("title", "")[:80]
                score = p.get("score", 0)
                src = p.get("source", "").upper()
                tldr = p.get("tldr", "")[:120]
                url = p.get("url", "")
                lines.append(f"  {i}. [{src}] {title}")
                lines.append(f"     Score: {score:.1f} | {tldr}")
                if url:
                    lines.append(f"     {url}")

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # HTML 邮件正文构建
    # ------------------------------------------------------------------

    def _format_html_body(self, result: RunResult) -> Optional[str]:
        """使用 HTML 模板生成邮件正文，模板不存在时返回 None"""
        template_name = "success" if result.success else "failure"
        template = _load_email_template(template_name)
        if not template:
            return None

        source_rows = self._build_source_rows_html(result)
        top_papers_html = self._build_top_papers_html(result)
        report_list_html = self._build_report_list_html(result)

        return _render_template(
            template,
            timestamp=result.run_timestamp,
            total_fetched=result.total_papers_fetched,
            total_qualified=result.total_qualified,
            total_analyzed=result.total_analyzed,
            source_rows=source_rows,
            top_papers_html=top_papers_html,
            report_list_html=report_list_html,
            error_message=self._html_escape(result.error_message or "无"),
            token_usage_html=self._format_token_section_html(result.token_usage),
        )

    def _format_html_error_body(self, template_name: str, **kwargs) -> Optional[str]:
        """使用 HTML 模板生成错误告警邮件正文，模板不存在时返回 None"""
        template = _load_email_template(template_name)
        if not template:
            return None
        escaped = {k: self._html_escape(str(v)) for k, v in kwargs.items()}
        return _render_template(template, **escaped)

    @staticmethod
    def _html_escape(text: str) -> str:
        """对文本进行 HTML 转义，防止特殊字符破坏结构"""
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )

    def _build_source_rows_html(self, result: RunResult) -> str:
        """构建数据来源统计表格行 HTML"""
        rows = []
        row_colors = ["#ffffff", "#f9fafb"]
        for i, source in enumerate(sorted(result.papers_by_source.keys())):
            fetched = result.papers_by_source.get(source, 0)
            qualified = result.qualified_by_source.get(source, 0)
            analyzed = result.analyzed_by_source.get(source, 0)
            bg = row_colors[i % 2]
            rows.append(
                f'<tr style="background-color:{bg};">'
                f'<td style="padding:10px 14px;font-size:13px;color:#374151;border-bottom:1px solid #f0f0f0;">'
                f'<span style="display:inline-block;background-color:#e0e7ff;color:#3730a3;'
                f'font-size:11px;font-weight:600;padding:2px 7px;border-radius:4px;">'
                f"{self._html_escape(source.upper())}</span></td>"
                f'<td style="padding:10px 14px;text-align:center;font-size:13px;font-weight:600;'
                f'color:#374151;border-bottom:1px solid #f0f0f0;">{fetched}</td>'
                f'<td style="padding:10px 14px;text-align:center;font-size:13px;font-weight:600;'
                f'color:#374151;border-bottom:1px solid #f0f0f0;">{qualified}</td>'
                f'<td style="padding:10px 14px;text-align:center;font-size:13px;font-weight:600;'
                f'color:#374151;border-bottom:1px solid #f0f0f0;">{analyzed}</td>'
                f"</tr>"
            )
        return (
            "\n".join(rows)
            if rows
            else (
                '<tr><td colspan="4" style="padding:14px;text-align:center;'
                'font-size:13px;color:#9ca3af;">暂无数据</td></tr>'
            )
        )

    def _build_top_papers_html(self, result: RunResult) -> str:
        """构建 Top-N 论文卡片 HTML（作为完整的 <tr> 块返回）"""
        if not result.top_papers:
            return ""

        cards = []
        for i, p in enumerate(result.top_papers, 1):
            title = self._html_escape(p.get("title", "")[:100])
            score = p.get("score", 0)
            src = self._html_escape(p.get("source", "").upper())
            tldr = self._html_escape(p.get("tldr", "")[:200])
            url = p.get("url", "")
            link_html = (
                (
                    f'<p style="margin:8px 0 0;">'
                    f'<a href="{self._html_escape(url)}" '
                    f'style="color:#5b6af0;font-size:12px;text-decoration:none;">查看原文 →</a></p>'
                )
                if url
                else ""
            )

            cards.append(
                f'<table width="100%" cellpadding="0" cellspacing="0" border="0" '
                f'style="margin-bottom:10px;border:1px solid #e8ebf0;border-radius:8px;'
                f'overflow:hidden;border-collapse:separate;">'
                f'<tr><td style="padding:14px 16px;background-color:#fafafa;border-bottom:1px solid #e8ebf0;">'
                f'<p style="margin:0;font-size:12px;color:#6b7280;">'
                f'<span style="background-color:#e0e7ff;color:#3730a3;font-size:11px;'
                f'font-weight:600;padding:1px 6px;border-radius:3px;margin-right:6px;">{src}</span>'
                f'Score: <strong style="color:#1a7a4a;">{score:.1f}</strong></p></td></tr>'
                f'<tr><td style="padding:14px 16px;">'
                f'<p style="margin:0 0 6px;font-size:14px;font-weight:600;color:#1a1f36;'
                f'line-height:1.4;">{i}. {title}</p>'
                f'<p style="margin:0;font-size:13px;color:#4b5563;line-height:1.6;">{tldr}</p>'
                f"{link_html}</td></tr>"
                f"</table>"
            )

        cards_html = "\n".join(cards)
        return (
            f'<tr><td style="padding:28px 32px 0;">'
            f'<h2 style="margin:0 0 14px;font-size:14px;font-weight:700;color:#1a1f36;'
            f"text-transform:uppercase;letter-spacing:1px;border-left:3px solid #5b6af0;"
            f'padding-left:10px;">Top {len(result.top_papers)} 论文</h2>'
            f"{cards_html}"
            f"</td></tr>"
        )

    def _build_report_list_html(self, result: RunResult) -> str:
        """构建报告路径列表 HTML（作为完整的 <tr> 块返回）"""
        if not result.report_paths:
            return ""

        rows = []
        row_colors = ["#ffffff", "#f9fafb"]
        for i, (source, path_str) in enumerate(sorted(result.report_paths.items())):
            bg = row_colors[i % 2]
            rows.append(
                f'<tr style="background-color:{bg};">'
                f'<td style="padding:10px 14px;font-size:12px;border-bottom:1px solid #f0f0f0;">'
                f'<span style="background-color:#e0e7ff;color:#3730a3;font-size:11px;'
                f'font-weight:600;padding:2px 7px;border-radius:4px;">'
                f"{self._html_escape(source.upper())}</span></td>"
                f'<td style="padding:10px 14px;font-size:12px;color:#6b7280;'
                f'font-family:monospace;word-break:break-all;border-bottom:1px solid #f0f0f0;">'
                f"{self._html_escape(path_str)}</td>"
                f"</tr>"
            )

        rows_html = "\n".join(rows)
        return (
            f'<tr><td style="padding:20px 32px 0;">'
            f'<h2 style="margin:0 0 12px;font-size:14px;font-weight:700;color:#1a1f36;'
            f"text-transform:uppercase;letter-spacing:1px;border-left:3px solid #5b6af0;"
            f'padding-left:10px;">报告路径</h2>'
            f'<table width="100%" cellpadding="0" cellspacing="0" border="0" '
            f'style="border-collapse:collapse;border:1px solid #e8ebf0;border-radius:8px;overflow:hidden;">'
            f"{rows_html}"
            f"</table></td></tr>"
        )

    def _collect_attachments(self, result: RunResult) -> List[Path]:
        """收集报告文件作为邮件附件"""
        attachments = []
        for source, path_str in result.report_paths.items():
            path = Path(path_str)
            if path.exists() and path.is_file():
                attachments.append(path)
        return attachments

    # ------------------------------------------------------------------
    # 研究趋势通知格式化
    # ------------------------------------------------------------------

    def _format_trend_subject(self, result: TrendRunResult) -> str:
        status = "SUCCESS" if result.success else "FAILED"
        keywords_str = ", ".join(result.keywords)
        return f"ArXiv Trend Research - {status} ({keywords_str}) ({result.run_timestamp})"

    def _format_trend_body(self, result: TrendRunResult) -> str:
        """向后兼容：默认使用通用模板（非 Telegram 专用）"""
        return self._format_trend_body_for_platform(result, None)

    def _format_trend_body_for_platform(
        self, result: TrendRunResult, platform: Optional[str]
    ) -> str:
        """使用模板格式化趋势分析通知正文"""
        if platform == "telegram":
            return self._format_telegram_trend_body(result)

        template_name = "research_success" if result.success else "research_failure"
        template = _load_template(template_name, platform=platform)

        keywords_str = ", ".join(result.keywords)
        date_range = f"{result.date_from} ~ {result.date_to}"

        # 报告路径
        report_lines = []
        if result.report_paths:
            report_lines.append("**报告路径**")
            for fmt, path in result.report_paths.items():
                report_lines.append(f"> `{fmt}` {path}")
        report_list = "\n".join(report_lines)

        if template:
            return _render_template(
                template,
                status="SUCCESS" if result.success else "FAILED",
                timestamp=result.run_timestamp,
                keywords=keywords_str,
                date_range=date_range,
                total_papers=result.total_papers,
                tldr_count=result.tldr_count,
                trend_skills_count=result.trend_skills_count,
                report_list=report_list,
                error_message=result.error_message or "无",
                token_usage_section=self._format_token_section_md(result.token_usage),
            )

        # 降级为纯文本
        return self._format_trend_body_fallback(result)

    def _format_telegram_trend_body(self, result: TrendRunResult) -> str:
        """Telegram 专用趋势分析 HTML 正文。"""
        status_label = "运行成功" if result.success else "运行失败"
        keywords_str = self._html_escape(", ".join(result.keywords))
        date_range = self._html_escape(f"{result.date_from} ~ {result.date_to}")

        report_lines = []
        for fmt, path in sorted(result.report_paths.items()):
            report_lines.append(f"<code>{self._html_escape(fmt.upper())}</code> {self._html_escape(path)}")

        sections = [
            "<b>ArXiv Trend Research</b>",
            f"<b>{status_label}</b> | {self._html_escape(result.run_timestamp)}",
            f"<b>关键词</b> {keywords_str}",
            f"<b>时间范围</b> {date_range}",
            (
                f"<b>统计</b> 论文 <b>{result.total_papers}</b> | TLDR <b>{result.tldr_count}</b> | "
                f"Skills <b>{result.trend_skills_count}</b>"
            ),
        ]

        if result.token_usage and result.token_usage.get("has_data") and self.settings.TOKEN_TRACKING_ENABLED:
            total = result.token_usage.get("total", 0)
            tp = result.token_usage.get("total_prompt", 0)
            tc = result.token_usage.get("total_completion", 0)
            sections.extend(
                [
                    "<b>Token 消耗</b>",
                    (
                        f"<blockquote>总计 <b>{total:,}</b> tokens"
                        f"（输入 {tp:,} / 输出 {tc:,}）</blockquote>"
                    ),
                ]
            )

        if report_lines:
            sections.extend(["<b>报告路径</b>", "\n".join(report_lines)])

        if not result.success and result.error_message:
            sections.extend(["<b>错误信息</b>", f"<blockquote>{self._html_escape(result.error_message)}</blockquote>"])

        return "\n".join(sections)

    def _format_error_body_for_platform(
        self, template_name: str, platform: Optional[str], **kwargs
    ) -> str:
        """按平台格式化错误告警正文，模板缺失时使用纯文本兜底。"""
        if platform == "telegram":
            return self._format_telegram_error_body(template_name, **kwargs)

        template = _load_template(template_name, platform=platform)
        if template:
            return _render_template(template, **kwargs)

        lines = [
            "## ArXiv Daily Researcher",
            "",
            f"**错误告警** | {kwargs.get('timestamp', '')}",
            "",
        ]
        for key, value in kwargs.items():
            if key != "timestamp":
                lines.append(f"> {key}: {value}")
        return "\n".join(lines)

    def _format_telegram_error_body(self, template_name: str, **kwargs) -> str:
        """Telegram 专用错误通知 HTML 正文。"""
        title_map = {
            "error_mineru": "MinerU 错误告警",
            "error_llm": "LLM 错误告警",
            "error_network": "网络错误告警",
            "error_generic": "通用错误告警",
        }
        title = title_map.get(template_name, "错误告警")

        timestamp = self._html_escape(str(kwargs.get("timestamp", "")))
        sections = [
            "<b>ArXiv Daily Researcher</b>",
            f"<b>{title}</b> | {timestamp}",
        ]
        for key, value in kwargs.items():
            if key == "timestamp":
                continue
            sections.append(f"<b>{self._html_escape(str(key))}</b>")
            sections.append(f"<blockquote>{self._html_escape(str(value))}</blockquote>")
        return "\n".join(sections)

    @staticmethod
    def _platform_for_notifier(notifier: BaseNotifier) -> Optional[str]:
        if isinstance(notifier, WebhookNotifier):
            return notifier.platform
        return None

    def _format_trend_body_fallback(self, result: TrendRunResult) -> str:
        """趋势通知模板不存在时的兜底纯文本"""
        status_icon = "OK" if result.success else "ERROR"
        lines = [
            f"Status: {status_icon}",
            f"Time: {result.run_timestamp}",
            f"Keywords: {', '.join(result.keywords)}",
            f"Date Range: {result.date_from} ~ {result.date_to}",
            "",
            f"Papers Found: {result.total_papers}",
            f"TLDRs Generated: {result.tldr_count}",
            f"Trend Skills: {result.trend_skills_count}",
        ]

        if result.error_message:
            lines.append("")
            lines.append(f"Error: {result.error_message}")

        if result.report_paths:
            lines.append("")
            lines.append("Reports:")
            for fmt, path in result.report_paths.items():
                lines.append(f"  [{fmt}] {path}")

        return "\n".join(lines)

    def _format_trend_html_body(self, result: TrendRunResult) -> Optional[str]:
        """使用 HTML 模板生成趋势分析邮件正文"""
        template_name = "research_success" if result.success else "research_failure"
        template = _load_email_template(template_name)
        if not template:
            return None

        keywords_str = self._html_escape(", ".join(result.keywords))
        date_range = self._html_escape(f"{result.date_from} ~ {result.date_to}")

        # 报告路径 HTML
        report_rows = []
        row_colors = ["#ffffff", "#f9fafb"]
        for i, (fmt, path_str) in enumerate(sorted(result.report_paths.items())):
            bg = row_colors[i % 2]
            report_rows.append(
                f'<tr style="background-color:{bg};">'
                f'<td style="padding:10px 14px;font-size:12px;border-bottom:1px solid #f0f0f0;">'
                f'<span style="background-color:#e0e7ff;color:#3730a3;font-size:11px;'
                f'font-weight:600;padding:2px 7px;border-radius:4px;">'
                f"{self._html_escape(fmt.upper())}</span></td>"
                f'<td style="padding:10px 14px;font-size:12px;color:#6b7280;'
                f'font-family:monospace;word-break:break-all;border-bottom:1px solid #f0f0f0;">'
                f"{self._html_escape(path_str)}</td>"
                f"</tr>"
            )
        report_rows_html = (
            "\n".join(report_rows)
            if report_rows
            else (
                '<tr><td colspan="2" style="padding:14px;text-align:center;'
                'font-size:13px;color:#9ca3af;">暂无报告</td></tr>'
            )
        )

        return _render_template(
            template,
            timestamp=self._html_escape(result.run_timestamp),
            keywords=keywords_str,
            date_range=date_range,
            total_papers=result.total_papers,
            tldr_count=result.tldr_count,
            trend_skills_count=result.trend_skills_count,
            report_rows_html=report_rows_html,
            error_message=self._html_escape(result.error_message or "无"),
            token_usage_html=self._format_token_section_html(result.token_usage),
        )

    def _collect_trend_attachments(self, result: TrendRunResult) -> List[Path]:
        """收集趋势报告文件作为邮件附件"""
        attachments = []
        for fmt, path_str in result.report_paths.items():
            path = Path(path_str)
            if path.exists() and path.is_file():
                attachments.append(path)
        return attachments
