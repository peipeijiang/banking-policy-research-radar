---
title: "MuSE：用于压力测试的多重宏观金融情景模拟引擎"
paper_id: "ecb:https://www.ecb.europa.eu//pub/pdf/scpwps/ecb.wp3270~4eb87cfa17.en.pdf"
source: "ecb"
published: "2026-08-05T09:00:00"
score: 70.0
tags: ["paper", "banking-fiscal-monetary-policy"]
---

# MuSE：用于压力测试的多重宏观金融情景模拟引擎

> **英文原标题**：MuSE: a multiple macro-financial scenario simulation engine for stress testing

[查看原文](https://www.ecb.europa.eu//pub/pdf/scpwps/ecb.wp3270~4eb87cfa17.en.pdf)

## 一句话结论

> 该论文设计了一个多宏观金融情景模拟引擎（MuSE），用于自上而下的压力测试，并评估欧元区银行在不利情景下的资本消耗。

## 论文信息

- **作者**：-
- **来源**：ECB Working Papers
- **发布时间**：2026-08-05
- **相关度评分**：70.0
- **DOI**：-

## 相关性评分

- **商业银行**：7.0/10（最高匹配）
- **货币政策**：4.0/10
- **财政政策**：3.0/10

<details open>
<summary><strong>中文摘要</strong></summary>

我们设计了一个计量经济学框架，用于模拟多种不利的宏观金融情景，这些情景可用于自上而下的压力测试。首先，我们构建了一个金融压力指数，该指数基于通过非参数copula在包含大量每日金融指标的数据集上估计所产生的冲击。其次，我们在一个大型多国贝叶斯向量自回归模型中，模拟了以基于copula的金融冲击为条件的宏观经济指标的联合动态变化。这一框架，我们称之为多重宏观金融压力情景模拟引擎（Multiple macro-financial stress scenario Simulation Engine，MuSE），使我们能够复制数千种宏观金融压力情景，在这些情景中，金融部门产生的不利冲击会传导至整体经济，引发显著的宏观经济波动。我们通过生成大量受过去危机启发的场景来展示其功能，这些场景涵盖了源自金融市场、主权债务和地缘政治紧张局势的压力。利用基于近期欧盟范围内压力测试的自上而下的偿付能力压力测试模型，我们预测了欧元区银行的资本消耗，并发现由股市和主权冲击引发的负面情景在当前时点似乎对欧元区银行业部门的韧性构成最大威胁。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

We design an econometric framework to simulate multiple adverse macro-financial scenarios that can be used in top-down stress tests. First, we create a financial stress index informed by shocks generated via a non-parametric copula estimated on a large dataset of daily financial indicators. Second, we simulate the joint dynamics of macroeconomic indicators conditional on the copula-based financial shocks in a large multi-country Bayesian VAR model. This framework,which we refer to as the Multiple macro-financial stress scenario Simulation Engine, MuSE, allows us to replicate thousands of macro-financial stress scenarios where adverse shocks generated in the financial sector propagate into the overall economy, triggering significant macroeconomic fluctuations. We demonstrate its functionality by generating a large number of scenarios inspired from past crises capturing stress stemming from financial markets, sovereign debt, and geopolitical tensions. Using a top-down solvency stress test model, based on recent EU-wide stress tests, we project the capital depletion for euro area banks and find that adverse scenarios triggered by stock market and sovereign shocks appear to threaten the resilience of the euro area banking sector the most at this juncture.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

本文设计了一个计量经济学框架，用于模拟可用于自上而下压力测试的多种不利宏观金融情景。首先，基于大量日度金融指标，通过非参数copula估计生成金融冲击，并构建金融压力指数。其次，在大型多国贝叶斯向量自回归（BVAR）模型中，以copula冲击为条件模拟宏观经济指标的联合动态。该框架（MuSE）能够复制数千种宏观金融压力情景，其中金融部门的冲击传导至整体经济，引发显著的宏观经济波动。作者通过生成受过去危机启发的多种情景（涵盖金融市场、主权债务和地缘政治紧张）展示了其功能，并利用基于近期欧盟压力测试的自上而下偿付能力压力测试模型，预测欧元区银行的资本消耗，发现股市和主权冲击引发的不利情景目前对欧元区银行业韧性威胁最大。

### 主要创新

- 提出MuSE框架，结合非参数copula、金融压力指数和大型多国BVAR，生成大量内部一致的宏观金融压力情景。
- 金融压力指数可向前预测一年，并可分解为各冲击驱动因素的贡献，便于识别压力来源。
- 利用BVAR模型将高频金融冲击传导至低频宏观经济变量，实现金融与宏观经济的有效连接。
- 通过重要性抽样和情景筛选，确保情景的严重性和与历史危机的一致性。
- 将生成的情景应用于银行压力测试，评估不同冲击对银行资本充足率的影响。

### 研究方法

论文采用三阶段方法：1）利用非参数copula对日度金融指标进行自助抽样，生成金融冲击路径；2）基于这些冲击构建金融压力指数（FSI），采用类似CISS的加权相关方法；3）将FSI作为外生变量纳入多国BVAR模型，使用Minnesota先验和t分布误差，通过Metropolis-Hastings-Gibbs采样估计，并利用卡尔曼滤波生成条件预测。

### 关键结果

生成的2008年型情景中，股市下跌最为严重；2011年型情景中，主权利差扩大最显著；2022年型情景中，短期利率上升明显。；在银行压力测试中，2008年型情景对欧元区银行资本充足率的负面影响最大，其次是2011年型情景。；2022年型情景因收益率曲线倒挂对银行盈利有利，资本消耗较低。；2025年型情景（法国主权债务扰动）对银行系统影响较小。；银行层面，G-SIBs和投资银行在2008年型情景下损失最大，而传统银行在2011年型情景下受影响更大。

### 技术栈

- 非参数copula
- 自助抽样（bootstrap）
- 金融压力指数（FSI）
- 指数加权移动平均（EWMA）
- 贝叶斯向量自回归（BVAR）
- Minnesota先验
- Metropolis-Hastings-Gibbs采样
- 卡尔曼滤波
- t分布误差

### 方法优势

- 方法创新，结合多种统计和计量工具，生成大量内部一致的情景。
- 金融压力指数可分解，有助于理解压力来源。
- BVAR模型能够捕捉金融与宏观经济的动态关系。
- 情景生成过程灵活，可针对不同风险叙事进行定制。
- 实证应用展示了框架在银行压力测试中的实用性。

### 主要局限

- 情景生成依赖于历史数据，可能无法完全捕捉新型风险。
- BVAR模型假设线性关系，可能无法刻画非线性效应。
- 金融压力指数的构建涉及主观选择（如变量、权重、衰减参数）。
- 银行压力测试模型基于历史弹性，可能无法反映当前银行资产负债表的变化。
- 未提供模型预测精度的正式评估。

### 与当前研究方向的关联

论文与关键词高度相关：涉及宏观金融情景校准、压力测试、金融机构韧性、贝叶斯技术、金融copula等。

---

_知识库更新时间：2026-08-06T03:57:42.792034_
