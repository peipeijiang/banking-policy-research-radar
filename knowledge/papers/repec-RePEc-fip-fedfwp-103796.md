---
title: "风险偏好与货币政策传导"
paper_id: "repec:RePEc:fip:fedfwp:103796"
source: "san_francisco_fed"
published: "2026-09-18T00:00:00"
score: 95.0
tags: ["paper", "banking-fiscal-monetary-policy"]
---

# 风险偏好与货币政策传导

> **英文原标题**：Risk Appetite and Monetary Transmission

[查看原文](https://ideas.repec.org/p/fip/fedfwp/103796.html)

## 一句话结论

> 论文构建了FOMC会议前后风险偏好变化的高频测度，利用代理SVAR识别风险偏好冲击和利率冲击，发现货币政策主要通过风险偏好和风险资产价格传导，而仅依赖利率意外的估计会遗漏大部分效应。

## 论文信息

- **作者**：Michael D. Bauer, Maik Schmeling, Andreas Schrimpf
- **来源**：Working Paper Series
- **发布时间**：2026-09-18
- **相关度评分**：95.0
- **DOI**：10.24148/wp2026-20

## 相关性评分

- **商业银行**：1.0/10
- **货币政策**：9.5/10（最高匹配）
- **财政政策**：0.0/10

<details open>
<summary><strong>中文摘要</strong></summary>

我们构建了一个新的高频指标，用于衡量联邦公开市场委员会（FOMC）会议前后风险偏好（risk appetite）的变动，即风险敏感指标变化的共同成分。美联储的政策行动和沟通对风险偏好具有实质性影响。利率意外（interest-rate surprises）仅能解释风险偏好变动的约五分之一，因此政策引发的风险资产价格变化大部分与预期利率路径正交。因此，我们在代理SVAR（proxy SVAR）中同时使用两种意外作为外部工具，并分别识别两种冲击。风险偏好冲击具有显著且持续的紧缩效应，会降低产出和价格，同时推高失业率。相比之下，无风险利率冲击的效应往往较小且估计不精确，部分结果符号令人困惑。货币传导似乎主要通过风险偏好和风险资产价格发挥作用。仅依赖利率意外的估计会遗漏大部分这些效应，原因有二：利率与风险偏好之间的联系具有状态依赖性，而美联储沟通对风险偏好的影响独立于预期利率路径。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

We construct a new high-frequency measure of risk appetite shifts around Federal Open Market Committee (FOMC) meetings, the common component of changes in risk-sensitive indicators. Fed policy actions and communication have substantial effects on risk appetite. Interest-rate surprises explain only about one-fifth of the variation in risk appetite, so most policy-induced changes in risk asset prices are orthogonal to the expected rate path. We therefore use both surprises as external instruments in a proxy SVAR with two separately identified shocks. Risk appetite shocks have large and persistent contractionary effects, lowering output and prices while raising unemployment. By contrast, the effects of risk-free rate shocks tend to be small and imprecisely estimated, and some have puzzling signs. Monetary transmission appears to operate primarily through risk appetite and risk asset prices. Estimates relying on interest-rate surprises alone miss most of these effects, for two reasons: the link from interest rates to risk appetite is state-dependent, and Fed communication moves it independently of the expected rate path.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

本文构建了一个新的高频风险偏好变动指标（RISK），该指标是FOMC会议前后十一种风险敏感资产价格变动的第一主成分，同时计算了基于无风险利率的传统货币政策意外（MPS）。研究发现，美联储政策行动和沟通对风险偏好有显著影响，但利率意外仅能解释RISK变动的约五分之一，大部分政策引发的风险资产价格变动与预期利率路径正交。作者将MPS和RISK作为外部工具，在代理SVAR中分别识别两种冲击。结果表明，风险偏好冲击对产出、价格和失业具有巨大且持久的收缩效应，而利率冲击的效应较小且不精确，部分符号令人困惑。货币政策传导主要通过风险偏好和风险资产价格发挥作用，仅依赖利率意外的估计会遗漏大部分效应，原因在于利率与风险偏好的联系具有状态依赖性，且美联储沟通能独立于预期利率路径影响风险偏好。

### 主要创新

- 构建了新的高频风险偏好变动指标（RISK），该指标是FOMC公告窗口内十一种风险敏感资产价格变动的第一主成分，且不施加与无风险利率意外正交的约束。
- 使用MPS和RISK作为两个外部工具，在代理SVAR中联合识别两种货币政策冲击：传统的利率冲击和风险偏好冲击。
- 发现风险偏好冲击在货币政策传导中占主导地位，而传统的利率冲击效应较小且不精确，甚至出现与教科书相反的符号。
- 通过叙事分析和对非政策安慰剂事件的检验，证明RISK变动主要由政策新闻驱动，而非信息效应。
- 揭示了利率与风险偏好联系的状态依赖性，以及美联储沟通独立于预期利率路径影响风险偏好的机制。

### 研究方法

论文采用高频识别方法，在FOMC公告窗口（从公告前15分钟至交易日结束）测量资产价格变动。使用主成分分析分别提取无风险利率意外（MPS）和风险偏好意外（RISK）。然后采用Stock和Watson（2012, 2018）的代理SVAR方法，以MPS和RISK作为外部工具，分别进行单工具识别和联合识别（遵循Mertens和Ravn, 2013），估计两种货币政策冲击对宏观经济变量的脉冲响应和预测误差方差分解。样本为1996年1月至2025年9月的245次FOMC公告，月度美国数据，VAR设定类似于Gertler和Karadi（2015）及Bauer和Swanson（2023b）。

### 关键结果

RISK解释了十一种风险敏感指标总方差的56.4%，MPS解释了五种无风险利率序列方差的76.6%。；MPS与RISK的相关系数为0.44，MPS仅能解释RISK变动的约19%（R²=0.19），大部分RISK变动与利率意外正交。；在单工具识别中，RISK冲击对产出、通胀和失业的效应比MPS冲击更大、更持久、更精确。；在联合识别中，RISK冲击导致工业产出持久下降、通胀下降、失业上升，且统计显著；而利率冲击效应较小且不精确，消费者价格反应温和，工业产出上升、失业下降，与教科书相反。；预测误差方差分解显示，在联合识别中，RISK冲击解释了工业产出、消费者价格和失业的无条件预测误差方差的约10-40%，而MPS冲击最多解释5%。；叙事分析表明，RISK的大幅变动大多可由美联储政策行动和沟通对风险偏好和风险感知的直接效应解释，仅2020年3月3日的事件可能符合信息效应。；非政策安慰剂事件中RISK的波动性显著更低，且与利率变动的相关性符号反转，表明政策新闻是RISK变动的主要驱动因素。

### 技术栈

- 主成分分析（PCA）
- 代理SVAR（proxy SVAR）
- 外部工具变量法
- 联合识别（Mertens和Ravn, 2013）
- 脉冲响应函数
- 预测误差方差分解
- 线性回归
- 叙事分析
- 高频事件窗口测量

### 方法优势

- 构建了高频、窄窗口的风险偏好指标，减少了其他新闻的混杂噪声，提高了信噪比。
- 不施加RISK与利率意外正交的约束，允许数据揭示利率与风险偏好的经验关系，从而更好地理解风险承担渠道。
- 使用两个外部工具联合识别两种冲击，能够分离利率渠道和风险渠道，提供更清晰的货币政策传导机制证据。
- 结合叙事分析，对极端事件进行深入解读，增强了结果的经济解释力。
- 样本覆盖时间长（1996-2025），包含245次FOMC公告，数据频率高，资产类别广泛。
- 发现风险偏好冲击在货币政策传导中占主导地位，对现有文献中过度关注利率冲击的做法提出了重要修正。

### 主要局限

- RISK指标虽然模型无关，但无法区分风险偏好变动与风险感知数量变动，两者可能都影响风险溢价。
- 高频窗口虽然减少了噪声，但仍可能受到其他同时发生的新闻影响，尽管作者通过安慰剂检验进行了验证。
- 联合识别依赖于两个工具的相关性结构，若工具与冲击的关系不稳定，识别可能受到影响。
- 样本期间包含零利率下限时期，可能影响利率冲击的估计。
- 叙事分析基于新闻覆盖，可能反映记者的事后解释而非真实机制，且仅针对极端事件。
- 论文主要关注美国数据，结论对其他经济体的外部有效性有待检验。

### 与当前研究方向的关联

本文与商业银行、财政政策与货币政策领域的最新学术研究高度相关。它直接涉及货币政策传导机制、中央银行政策工具（如利率和沟通）、风险承担渠道、金融中介（如交易商资产负债表约束）、金融稳定和信用周期。论文使用高频识别和代理SVAR方法，具有明确的识别策略和稳健性检验，政策含义显著，且提供了公开的工作论文全文。因此，该论文与关键词中的货币政策、银行信贷与风险承担、金融中介、中央银行政策工具、金融稳定等高度契合。

<details>
<summary><strong>发现与关联证据</strong></summary>

- **provider**：IDEAS/RePEc
- **series_url**：https://ideas.repec.org/s/fip/fedfwp.html
- **free_download**：True
- **date_precision**：day

</details>

---

_知识库更新时间：2026-09-24T05:23:18.144713_
