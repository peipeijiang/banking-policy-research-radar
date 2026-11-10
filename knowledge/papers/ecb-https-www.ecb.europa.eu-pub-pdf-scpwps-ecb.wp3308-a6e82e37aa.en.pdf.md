---
title: "释放信用风险监管有效性：来自欧洲央行监管发现与措施的洞见"
paper_id: "ecb:https://www.ecb.europa.eu//pub/pdf/scpwps/ecb.wp3308~a6e82e37aa.en.pdf"
source: "ecb"
published: "2026-11-09T10:00:00"
score: 90.0
tags: ["paper", "banking-fiscal-monetary-policy"]
---

# 释放信用风险监管有效性：来自欧洲央行监管发现与措施的洞见

> **英文原标题**：Unlocking supervisory effectiveness in credit risk: insights from the ECB’s supervisory findings and measures

[查看原文](https://www.ecb.europa.eu//pub/pdf/scpwps/ecb.wp3308~a6e82e37aa.en.pdf)

## 一句话结论

> 论文利用ECB银行监管保密数据（2016-2025年8106项监管措施），基于LLM构建监管有效性指标，通过逻辑和久期模型分析信用风险监管措施整改结果与速度的驱动因素，发现多维度发现、数据/报告/IT类措施及现场检查来源和治理强度显著影响整改成效。

## 论文信息

- **作者**：-
- **来源**：ECB Working Papers
- **发布时间**：2026-11-09
- **相关度评分**：90.0
- **DOI**：-

## 相关性评分

- **商业银行**：9.0/10（最高匹配）
- **货币政策**：2.0/10
- **财政政策**：0.5/10

<details open>
<summary><strong>中文摘要</strong></summary>

本文利用欧洲央行银行监管的保密数据，对信用风险领域的监管有效性进行了评估。分析覆盖了2016年至2025年间发布并关闭的8，106项监管措施。本文的核心贡献在于构建了一个措施层面的监管有效性指标，该指标基于大语言模型（LLM）对监管叙述和关闭理由的分析。该指标捕捉了监管措施是否实现了对 underlying deficiencies（根本性缺陷）的完全整改。我们运用逻辑模型和持续时间模型，考察了与整改结果和整改速度相关的发现、措施和银行特征。结果表明，多方面的发现是监管结果的关键驱动因素。与数据、报告和IT缺陷相关的措施实现完全整改的可能性较低，且需要更长的整改周期。源自现场检查的措施与更高的整改率和更快的关闭相关。更强的治理水平也与更成功的整改结果相关。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

This paper provides an assessment of supervisory effectiveness in credit risk using confidential data from ECB Banking Supervision. The analysis covers 8,106 supervisory measures issued and closed between 2016 and 2025. A central contribution is the construction of a measure level indicator of supervisory effectiveness based on large language model (LLM) analysis of supervisory narratives and closure justifications. The indicator captures whether supervisory measures resulted in full remediation of the underlying deficiencies. Using logistic and duration models, we examine the characteristics of findings, measures, and banks associated with remediation outcomes and remediation speed. The results show that multi-faceted findings are a key driver of supervisory outcomes. Measures related to data, reporting, and IT deficiencies are less likely to achieve full remediation and require longer remediation periods. Measures originating from on-site inspections are associated with higher remediation rates and faster closure. Stronger governance is also associated with more successful remediation outcomes.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

本文利用欧洲央行银行业监管的保密数据，评估信用风险领域的监管有效性。分析覆盖2016至2025年间发布并关闭的8,106项监管措施。核心贡献在于基于大语言模型（LLM）对监管叙述和关闭理由的分析，构建了措施层面的监管有效性指标，该指标捕捉监管措施是否导致底层缺陷的完全修复。研究采用逻辑回归和久期模型，考察与修复结果和修复速度相关的发现、措施及银行特征。结果表明，多层面发现是监管结果的关键驱动因素；涉及数据、报告和IT缺陷的措施更难实现完全修复且需要更长修复期；源自现场检查的措施修复率更高、关闭更快；更强的治理也与更成功的修复结果相关。

### 主要创新

- 首次在单项监管措施层面（而非监管框架或工具层面）进行大规模监管有效性的实证评估。
- 基于LLM分析监管叙述和关闭理由，构建了以修复结果为导向的新型监管有效性指标，区分完全修复、部分修复和未修复。
- 展示了如何利用人工智能从大量保密监管文本中提取政策相关信息，扩展了银行业监管实证研究和政策评估的范围。
- 将监管发现和措施通过LLM分类框架归入六个修复主题类别，并构建发现类型和主题数量等结构化变量。

### 研究方法

研究首先使用GPT-4.1模型，以提示词框架对每项监管措施的描述和关闭叙述进行分类，将措施判定为有效（完全修复）、部分有效（部分修复）或无效（未修复）；温度参数设为0.15，重复分类十次并以多数投票规则汇总，同时使用o4-mini模型复现，一致率约90%。随后将监管发现和措施分类为六个修复主题类别。实证策略上，采用二项逻辑回归分析完全修复的驱动因素，因变量为是否有效（完全修复=1，部分有效或无效=0），控制发现与措施特征、银行特征及年份固定效应；稳健性检验包括引入JST和国别固定效应、排除无效措施、以及多分类逻辑回归。进一步使用Cox比例风险模型分析有效措施的持续时间，并以加速失效时间（AFT）模型作为稳健性补充。

### 关键结果

发现复杂性是监管结果的重要决定因素：涉及多个主题的发现显著更不可能实现完全修复，且措施保持开放的时间更长。；相对于数据、报告与IT类发现，治理与控制、分类与分阶段、拨备与模型风险、信用生命周期管理类措施实现完全修复的可能性更高；NPE与抵押品管理类发现无统计显著差异。；源自现场检查的措施比源自SREP或其他JST活动的措施具有更高的修复率和更短的修复期。；建议类措施比义务类措施更可能实现完全修复；高严重程度（M3）和极高严重程度（M4）措施实现完全修复的可能性显著更低。；银行治理较弱（SREP治理评分较高）与完全修复可能性较低相关；信用风险重要性和盈利能力较高的银行在基准模型中更可能实现完全修复，但引入JST固定效应后银行特征失去显著性。

### 技术栈

- GPT-4.1大语言模型（提示词框架、温度参数0.15）
- o4-mini模型（替代模型复现验证）
- 多数投票规则（十次重复分类聚合）
- 二项逻辑回归（Logit）
- 多分类逻辑回归（Multinomial Logit）
- Cox比例风险模型
- 加速失效时间模型（AFT）
- 固定效应（年份、JST、国别）

### 方法优势

- 利用保密监管数据，覆盖8,106项信用风险相关监管措施，样本规模大且信息丰富。
- 创新性地将LLM应用于保密监管文本，构建措施层面的结果导向有效性指标，弥补了传统过程型监管绩效指标的不足。
- 进行了多轮验证：人工在环验证、十次重复多数投票、替代模型复现（一致率约90%），增强了指标可靠性。
- 实证策略较为稳健，包含JST和国别固定效应、排除无效措施、多分类逻辑回归以及AFT模型等多种稳健性检验。
- 研究结论具有明确的政策含义，可支持监管当局设计更聚焦的监管措施、分配资源和校准监管强度。

### 主要局限

- 研究为观察性分析，结果应解释为条件关联而非因果效应，存在措施非随机分配、遗漏变量和监管强度异质性等内生性问题。
- 有效性分类依赖于监管叙述的完整性和清晰度，可能受报告实践影响；提示词方法对指令设计和模型特定行为敏感。
- 指标捕捉的是有记录的修复情况，而非监管措施对银行风险的更广泛影响。
- 样本经过筛选，可能不能完全代表更广泛的监管措施总体；排除内部模型调查发现和2026年措施。
- Cox模型样本仅包含完全有效措施，无删失观测，限制了其比较已完成与仍在进行措施的核心优势；估计效应以成功完成为条件。

### 与当前研究方向的关联

本文与银行信贷与风险承担、资本和流动性监管、金融中介、宏观审慎政策、金融稳定和信用周期等关键词高度相关。研究聚焦信用风险领域的监管有效性，直接涉及银行信贷风险管理、监管措施对缺陷修复的影响以及银行治理和风险承担行为。使用欧洲央行保密监管数据和大语言模型方法，属于银行监管与金融稳定研究的交叉领域，对理解监管工具如何促进银行修复信用风险缺陷具有政策意义。

---

_知识库更新时间：2026-11-10T07:45:46.613133_
