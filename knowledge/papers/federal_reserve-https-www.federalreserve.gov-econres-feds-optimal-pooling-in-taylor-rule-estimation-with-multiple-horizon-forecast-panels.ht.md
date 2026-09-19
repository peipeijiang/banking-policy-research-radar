---
title: "多期限预测面板下泰勒规则估计中的最优池化"
paper_id: "federal_reserve:https://www.federalreserve.gov/econres/feds/optimal-pooling-in-taylor-rule-estimation-with-multiple-horizon-forecast-panels.htm"
source: "federal_reserve"
published: "2026-09-18T20:10:00"
score: 85.0
tags: ["paper", "banking-fiscal-monetary-policy"]
---

# 多期限预测面板下泰勒规则估计中的最优池化

> **英文原标题**：FEDS Paper: Optimal Pooling in Taylor Rule Estimation with Multiple-Horizon Forecast Panels

[查看原文](https://www.federalreserve.gov/econres/feds/optimal-pooling-in-taylor-rule-estimation-with-multiple-horizon-forecast-panels.htm)

## 一句话结论

> 论文将多期限预测面板中的池化结构作为推断对象，通过贝叶斯边际似然比较不同池化模式，发现政策利率预测的系统性变化主要来自随预测期限和调查日期变化的截距项，而时变响应系数的证据较弱。

## 论文信息

- **作者**：-
- **来源**：Federal Reserve FEDS and IFDP
- **发布时间**：2026-09-18
- **相关度评分**：85.0
- **DOI**：-

## 相关性评分

- **商业银行**：0.0/10
- **货币政策**：8.5/10（最高匹配）
- **财政政策**：0.0/10

<details open>
<summary><strong>中文摘要</strong></summary>

Edward Herbst和Karen Page多期预测面板（multiple-horizon forecast panels）越来越多地被用于推断感知到的货币政策规则，但推断结果取决于系数如何跨预测者、日期和预测期进行合并。我们将这种合并结构本身作为推断对象。在一个参与者-日期-预测期的泰勒规则回归模型中，我们使用贝叶斯边际似然比较不同的合并模式，并将该框架应用于Blue Chip Financial Forecasts、Survey of Professional Forecasters和Summary of Economic Projections。优选设定将政策利率预测中的大部分系统性变异归因于随预测期和调查日期变化的截距项。通过具有经济意义的时间变化响应系数来证明货币政策“认知变化”的证据总体上较为薄弱。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Edward Herbst and Karen Page Multiple-horizon forecast panels are increasingly used to infer perceived monetary policy rules, but inference depends on how coefficients are pooled across forecasters, dates, and horizons. We treat this pooling structure as the object of inference. In a participant-date-horizon Taylor-rule regression model, we compare pooling patterns using Bayesian marginal likelihoods, applying the framework to the Blue Chip Financial Forecasts, Survey of Professional Forecasters, and the Summary of Economic Projections. The preferred specifications place much of the systematic variation in policy-rate forecasts in intercepts that vary across forecast horizons and survey dates. Evidence of "changing perceptions" of monetary policy via economically meaningful time-varying response coefficients is weak overall.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

本文研究多期限预测面板中泰勒规则估计的池化结构问题。作者指出，现有文献通常预先设定系数在预测者、预测期限和调查日期之间的变化方式，并将替代设定作为稳健性检验，但完全无限制的规则无法识别。论文将池化模式本身作为推断对象，在预测者-日期-期限的泰勒规则回归中，枚举所有可能的池化模式，并采用贝叶斯边际似然比较各模式。作者将该问题转化为变量选择问题，利用g先验和hyper-g/n先验进行模型比较，并应用于Blue Chip Financial Forecasts、Survey of Professional Forecasters和Summary of Economic Projections三个数据集。主要结论是：三个数据集均拒绝常系数规则，最优设定将政策利率预测的系统性变异主要归入随预测期限和调查日期变化的截距项，而反应系数存在经济意义时变的证据较弱。

### 主要创新

- 将泰勒规则估计中的池化结构作为推断对象，而非预先设定，系统枚举所有可能的池化模式。
- 将池化模式选择问题转化为贝叶斯变量选择问题，利用边际似然进行模型比较。
- 采用g先验和hyper-g/n先验处理模型空间大且非嵌套的模型选择问题，避免Bartlett悖论。
- 将框架扩展到惯性规则和部分池化，模型空间从数百扩大到数十亿。
- 首次将系数异质性作为贝叶斯变量选择问题处理，并应用于三个主要预测面板。

### 研究方法

论文建立预测者-日期-期限的泰勒规则回归模型，允许截距、活动响应系数和通胀响应系数在预测者、期限和日期三个维度上变化。对于每个系数，定义其池化模式为所变化的维度子集，排除完全无限制的不可识别模式。将池化模式选择转化为贝叶斯变量选择问题，使用g先验对系数异质性部分进行先验设定，并采用hyper-g/n先验对g进行积分，得到边际似然的闭式表达。通过计算各池化模式的后验概率进行模型比较。进一步将框架扩展到惯性规则，允许滞后政策利率系数也进行池化，模型空间扩大至2401个候选模型。

### 关键结果

三个数据集均拒绝常系数泰勒规则，支持存在 considerable 异质性。；最优池化模式均不采用Bauer et al. (2024)的预测者-日期截距、日期反应系数设定。；基线静态设定下，三个面板均选择随预测期限和调查日期变化的截距，而非随预测者变化。；反应系数的时变证据较弱，最优设定常将反应系数跨日期池化，或时变幅度较小。；预测期限是泰勒规则系数异质性的重要来源。；惯性规则下，大部分预测路径变异被归入持久性，直接响应系数影响更小。；部分池化下，反应系数变异压缩为少数机制和期限组。

### 技术栈

- 贝叶斯模型选择
- 边际似然
- g先验
- hyper-g/n先验
- Appell超几何函数
- QR分解
- 变量选择
- 后验模型概率
- 贝叶斯模型平均

### 方法优势

- 将池化结构作为推断对象，避免预先设定带来的偏差。
- 贝叶斯框架能够处理大且非嵌套的模型空间，提供清晰的拟合与简约性权衡。
- 利用g先验的解析可处理性，边际似然有闭式表达，计算可行。
- 应用于三个主要预测面板，结论具有稳健性。
- 扩展框架到惯性规则和部分池化，增强适用性。

### 主要局限

- 论文主要关注池化模式的选择，未深入探讨经济结构模型的识别问题。
- SEP数据样本较短，参与者数量有限，可能影响推断的精确性。
- 部分池化扩展中模型空间巨大，计算负担较重。
- 论文未提供所有数据集的完整复现材料或代码。
- 对预测期限和日期的具体经济解释有限。

### 与当前研究方向的关联

论文与货币政策、中央银行政策工具、利率与通胀等关键词高度相关。它研究泰勒规则估计中系数池化结构，涉及货币政策反应函数的推断，直接关联中央银行政策工具和利率预期。同时，论文使用预测面板数据，涉及通胀和活动预测，与通胀和利率研究相关。此外，论文的贝叶斯模型选择方法对宏观审慎政策和金融稳定研究也有方法论借鉴意义。

---

_知识库更新时间：2026-09-19T05:01:12.123698_
