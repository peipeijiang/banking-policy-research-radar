---
title: "货币政策中的风险与不确定性"
paper_id: "federal_reserve:https://www.federalreserve.gov/econres/feds/risks-and-uncertainty-in-monetary-policy.htm"
source: "federal_reserve"
published: "2026-09-01T19:56:00"
score: 80.0
tags: ["paper", "banking-fiscal-monetary-policy"]
---

# 货币政策中的风险与不确定性

> **英文原标题**：FEDS Paper: Risks and Uncertainty in Monetary Policy

[查看原文](https://www.federalreserve.gov/econres/feds/risks-and-uncertainty-in-monetary-policy.htm)

## 一句话结论

> 该论文提出一种将货币政策情景分析与分布预测统一起来的框架，通过Scenario Synthesis方法为风险评估和政策制定提供可复现的工具。

## 论文信息

- **作者**：-
- **来源**：Federal Reserve FEDS and IFDP
- **发布时间**：2026-09-01
- **相关度评分**：80.0
- **DOI**：-

## 相关性评分

- **商业银行**：0.0/10
- **货币政策**：8.0/10（最高匹配）
- **财政政策**：0.0/10

<details open>
<summary><strong>中文摘要</strong></summary>

Tobias Adrian、Domenico Giannone、Matteo Luciani 和 Mike West 指出，中央银行通过两种传统方式来监测宏观经济风险：一种是自20世纪90年代中期以来经常使用的情景分析（scenario analysis），另一种则是自20世纪60年代末开始实践的分布预测（distributional forecasting）。这两种方法互为补充但又彼此独立：情景分析提供了缺乏概率的叙事，而预测分布则提供了经济解释有限的概率。将基准预测和情景视为条件预测密度（conditional predictive densities），并将分布预测视为参考预测分布（reference predictive distributions），可以将两者置于一个统一的框架内，并厘清它们各自的角色。情景综合法（Scenario Synthesis）为情景赋予与参考分布相一致的权重，从而为深度不确定性下的风险评估和政策审议提供了一种实用且可复现的工具。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Tobias Adrian, Domenico Giannone, Matteo Luciani , and Mike West Central banks monitor macroeconomic risk through two traditions: scenario analysis, regularly used since the mid-1990s, and distributional forecasting, practiced since the late 1960s. The two are complementary but separate: scenarios provide narratives without probabilities, while predictive distributions provide probabilities with limited economic interpretation. Treating baseline forecasts and scenarios as conditional predictive densities, and distributional forecasts as reference predictive distributions, places both within a common framework and clarifies their roles. The Scenario Synthesis assigns weights to scenarios consistent with the reference distribution, offering a practical and reproducible tool for risk assessment and policy deliberation under deep uncertainty.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

本文回顾了中央银行通过情景分析和预测分布监测宏观经济风险的两种传统，指出二者互补但分离：情景提供叙事但无概率，预测分布提供概率但缺乏经济解释。作者提出将基线预测和情景视为条件预测密度，将分布预测视为参考预测分布，从而统一框架，并开发了“情景综合”方法，根据参考分布为情景分配权重，提供可复现的风险评估工具。文章通过美联储2007年12月和2018年12月Tealbook数据的实证应用，展示了该方法如何评估情景集是否覆盖相关风险，并为政策讨论提供纪律。

### 主要创新

- 提出将基线预测和情景视为条件预测密度，将分布预测视为参考预测分布的统一框架。
- 开发“情景综合”方法，通过一致性准则为情景分配概率权重，使情景与预测分布相互关联。
- 提供历史视角，梳理美联储及其他央行风险分析实践的演变。
- 实证应用显示该方法能评估情景集的风险覆盖程度，并指导改进情景设计。

### 研究方法

本文采用理论框架构建与实证应用相结合的方法。首先，从历史角度回顾美联储及其他央行的风险分析实践，区分情景分析和预测分布。其次，提出将基线预测和情景视为条件预测密度，将参考预测分布视为无条件分布的框架，并基于贝叶斯预测综合（Bayesian Predictive Synthesis）提出情景综合方法，通过最小化综合分布与参考分布之间的差异（如KL散度）来求解情景权重。最后，使用美联储2007年12月和2018年12月的Tealbook数据（包括情景和预测分布）进行实证分析，评估情景综合的效果。

### 关键结果

实证结果显示，在2007年12月，情景集对GDP增长下行风险的覆盖有限（信贷紧缩情景捕获了一定概率质量，但2008-09年的实际结果左尾更厚），且不同参考密度导致权重差异显著。在2018年12月，情景集更接近覆盖相关风险，产生了内部一致的风险评估。此外，文章还展示了情景综合可用于评估风险平衡、情景集是否覆盖风险，并指导改进情景设计。

### 技术栈

- 贝叶斯预测综合（Bayesian Predictive Synthesis）、KL散度（Kullback-Leibler divergence）、条件预测密度、参考预测分布、情景分析、预测分布、FRB/US模型、DSGE模型、BVAR模型、Growth-at-Risk框架、分位数回归、时间序列模型。

### 方法优势

- 提供了统一的理论框架，将情景分析和预测分布联系起来，弥补了实践中的概念鸿沟。
- 历史回顾详尽，有助于理解两种方法的起源和演变。
- 实证应用展示了方法的实用性，能够为政策制定提供量化风险评估。
- 方法具有可复制性，有助于提高风险评估的透明度和纪律性。

### 主要局限

- 输入内容未提供明确的局限性讨论，但可推断：情景综合的权重依赖于参考分布的选择，不同参考分布可能导致不同权重；情景集可能无法完全覆盖所有风险，导致综合结果偏差；方法需要高质量的情景和预测分布数据，实际应用中可能面临数据可得性和模型不确定性挑战。

### 与当前研究方向的关联

本文与关键词高度相关：研究聚焦于货币政策中的风险与不确定性，涉及中央银行政策工具、金融稳定、宏观审慎政策等。具体而言，文章讨论了美联储、欧洲央行、英国央行等中央银行的货币政策实践，分析了情景分析和预测分布等工具在风险评估中的应用，并提出了改进方法，对货币政策制定和金融稳定评估具有重要参考价值。

---

_知识库更新时间：2026-09-02T05:01:53.292385_
