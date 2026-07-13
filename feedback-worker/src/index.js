const encoder = new TextEncoder();

function response(body, init = {}) {
  return new Response(body, {
    ...init,
    headers: {
      "content-type": "text/html; charset=utf-8",
      "cache-control": "no-store",
      "x-content-type-options": "nosniff",
      ...(init.headers || {}),
    },
  });
}

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
      "x-content-type-options": "nosniff",
    },
  });
}

function bytesToHex(bytes) {
  return [...new Uint8Array(bytes)].map((byte) => byte.toString(16).padStart(2, "0")).join("");
}

async function signatureFor(secret, action, paperId) {
  const key = await crypto.subtle.importKey(
    "raw",
    encoder.encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  return bytesToHex(await crypto.subtle.sign("HMAC", key, encoder.encode(`${action}\n${paperId}`)));
}

function timingSafeEqual(left, right) {
  if (left.length !== right.length) return false;
  let mismatch = 0;
  for (let index = 0; index < left.length; index += 1) {
    mismatch |= left.charCodeAt(index) ^ right.charCodeAt(index);
  }
  return mismatch === 0;
}

async function validate(request, env) {
  const url = new URL(request.url);
  const action = url.searchParams.get("action") || "";
  const paperId = url.searchParams.get("paper_id") || "";
  const supplied = url.searchParams.get("sig") || "";
  if (!env.FEEDBACK_SIGNING_SECRET || !["LIKE", "IGNORE"].includes(action) || !paperId || !supplied) {
    return null;
  }
  const expected = await signatureFor(env.FEEDBACK_SIGNING_SECRET, action, paperId);
  return timingSafeEqual(supplied, expected) ? { action, paperId, url } : null;
}

function landingPage(requestUrl, action) {
  const label = action === "LIKE" ? "喜欢" : "忽略";
  const endpoint = JSON.stringify(requestUrl).replaceAll("<", "\\u003c");
  return `<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>记录论文反馈</title><style>
body{margin:0;min-height:100vh;display:grid;place-items:center;background:#f5f5f7;color:#1d1d1f;font:16px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
main{width:min(88vw,420px);text-align:center}h1{font-size:28px;margin:0 0 12px}p{color:#6e6e73;line-height:1.6}.mark{font-size:44px;margin-bottom:16px}.error{color:#b42318}
</style></head><body><main><div class="mark" id="mark">...</div><h1 id="title">正在记录“${label}”</h1><p id="message">完成后可以直接关闭此页面。</p></main>
<script>
fetch(${endpoint},{method:"POST",headers:{"content-type":"application/json"}}).then(async r=>{const d=await r.json();if(!r.ok)throw new Error(d.error||"记录失败");document.getElementById("mark").textContent="✓";document.getElementById("title").textContent=d.already_recorded?"已经记录过":"反馈已记录";document.getElementById("message").textContent="你可以直接关闭此页面。"}).catch(e=>{document.getElementById("mark").textContent="!";document.getElementById("title").textContent="记录失败";document.getElementById("title").className="error";document.getElementById("message").textContent=e.message});
</script></body></html>`;
}

async function githubRequest(env, path, init = {}) {
  return fetch(`https://api.github.com/repos/${env.GITHUB_REPOSITORY}${path}`, {
    ...init,
    headers: {
      accept: "application/vnd.github+json",
      authorization: `Bearer ${env.GITHUB_TOKEN}`,
      "user-agent": "arxiv-research-feedback-worker",
      "x-github-api-version": "2022-11-28",
      ...(init.headers || {}),
    },
  });
}

async function recordFeedback(env, action, paperId) {
  if (!env.GITHUB_TOKEN || !env.GITHUB_REPOSITORY) {
    throw new Error("反馈服务尚未完成 GitHub 配置");
  }
  const issuesResponse = await githubRequest(
    env,
    "/issues?state=all&labels=paper-feedback&per_page=100&sort=created&direction=desc",
  );
  if (!issuesResponse.ok) throw new Error("无法读取现有反馈");
  const issues = await issuesResponse.json();
  const latest = issues.find((issue) => {
    const match = /^\[(LIKE|IGNORE)\]\s+(.+)$/.exec(issue.title || "");
    return match && match[2] === paperId;
  });
  if (latest && latest.title === `[${action}] ${paperId}`) {
    return { already_recorded: true, issue_number: latest.number };
  }
  const createResponse = await githubRequest(env, "/issues", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      title: `[${action}] ${paperId}`,
      labels: ["paper-feedback"],
      body: "Recorded automatically from the WeCom one-click feedback link.",
    }),
  });
  if (!createResponse.ok) throw new Error("GitHub 反馈写入失败");
  const issue = await createResponse.json();
  return { already_recorded: false, issue_number: issue.number };
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/health") return jsonResponse({ ok: true });
    if (url.pathname !== "/feedback") return response("Not found", { status: 404 });

    const input = await validate(request, env);
    if (!input) return response("Invalid or unsigned feedback link", { status: 403 });
    if (request.method === "GET") return response(landingPage(request.url, input.action));
    if (request.method !== "POST") return jsonResponse({ error: "Method not allowed" }, 405);

    try {
      return jsonResponse(await recordFeedback(env, input.action, input.paperId));
    } catch (error) {
      return jsonResponse({ error: error.message || "记录失败" }, 502);
    }
  },
};
