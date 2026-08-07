---
title: "MuSE：用于压力测试的多重宏观金融情景模拟引擎"
paper_id: "repec:RePEc:ecb:ecbwps:20263270"
source: "ecb_repec"
published: "2026-08-01T00:00:00"
score: 70.0
tags: ["paper", "banking-fiscal-monetary-policy"]
---

# MuSE：用于压力测试的多重宏观金融情景模拟引擎

> **英文原标题**：MuSE: a multiple macro-financial scenario simulation engine for stress testing

[查看原文](https://ideas.repec.org/p/ecb/ecbwps/20263270.html)

## 一句话结论

> 本文设计了一个多国宏观金融压力情景模拟引擎（MuSE），用于自上而下的压力测试，并评估欧元区银行在多种不利情景下的资本消耗。

## 论文信息

- **作者**：Bräutigam, Marcel, Figueres, Juan Manuel, Giglio, Carla, Grassi, Alberto, Prieto, Barbara Montero, Rodriguez d’Acri, Costanza, Salleo, Carmelo
- **来源**：Working Paper Series
- **发布时间**：2026-08-01
- **相关度评分**：70.0
- **DOI**：-

## 相关性评分

- **商业银行**：7.0/10（最高匹配）
- **货币政策**：4.0/10
- **财政政策**：3.0/10

<details open>
<summary><strong>中文摘要</strong></summary>

我们设计了一个计量经济学框架，用于模拟多种不利的宏观金融情景，这些情景可用于自上而下的压力测试。首先，我们构建了一个金融压力指数，该指数基于通过非参数copula在包含大量每日金融指标的数据集上估计生成的冲击。其次，我们在一个大型多国贝叶斯向量自回归模型中，模拟了以基于copula的金融冲击为条件的宏观经济指标的联合动态。这一框架，我们称之为多重宏观金融压力情景模拟引擎（Multiple macro-financial stress scenario Simulation Engine，MuSE），使我们能够复制数千种宏观金融压力情景，在这些情景中，金融部门产生的不利冲击会传导至整体经济，引发显著的宏观经济波动。我们通过生成大量受过去危机启发的场景来展示其功能，这些场景涵盖了源自金融市场、主权债务和地缘政治紧张局势的压力。利用基于近期欧盟范围内压力测试的自上而下偿付能力压力测试模型，我们预测了欧元区银行的资本消耗，并发现由股票市场和主权冲击引发的不利情景在当前时点似乎对欧元区银行业的韧性构成最大威胁。JEL分类号：C15, G01, G17, G21

</details>

<details>
<summary><strong>英文摘要</strong></summary>

We design an econometric framework to simulate multiple adverse macro-financial scenarios that can be used in top-down stress tests. First, we create a financial stress index informed by shocks generated via a non-parametric copula estimated on a large dataset of daily financial indicators. Second, we simulate the joint dynamics of macroeconomic indicators conditional on the copula-based financial shocks in a large multi-country Bayesian VAR model. This framework,which we refer to as the Multiple macro-financial stress scenario Simulation Engine, MuSE, allows us to replicate thousands of macro-financial stress scenarios where adverse shocks generated in the financial sector propagate into the overall economy, triggering significant macroeconomic fluctuations. We demonstrate its functionality by generating a large number of scenarios inspired from past crises capturing stress stemming from financial markets, sovereign debt, and geopolitical tensions. Using a top-down solvency stress test model, based on recent EU-wide stress tests, we project the capital depletion for euro area banks and find that adverse scenarios triggered by stock market and sovereign shocks appear to threaten the resilience of the euro area banking sector the most at this juncture. JEL Classification: C15, G01, G17, G21

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

本文设计了一个计量经济学框架，用于模拟可用于自上而下压力测试的多种不利宏观金融情景。首先，基于大量日度金融指标，通过非参数copula估计生成金融冲击，并构建金融压力指数。其次，在大型多国贝叶斯向量自回归（BVAR）模型中，以copula金融冲击为条件，模拟宏观经济指标的联合动态。该框架称为多重宏观金融压力情景模拟引擎（MuSE），能够复制数千种宏观金融压力情景，其中金融部门产生的不利冲击会传导至整体经济，引发显著的宏观经济波动。作者通过生成大量受过去危机启发的、涵盖金融市场、主权债务和地缘政治紧张局势压力的情景，展示了其功能。利用基于近期欧盟范围压力测试的自上而下偿付能力压力测试模型，作者预测了欧元区银行的资本消耗，发现股市和主权冲击引发的不利情景目前对欧元区银行业韧性威胁最大。

### 主要创新

- 提出MuSE框架，结合非参数copula、金融压力指数和大型多国BVAR，生成大量内部一致的宏观金融压力情景。
- 金融压力指数可向前预测一年，并可分解为各压力因子的贡献，便于识别情景的主要驱动因素。
- 采用重要性抽样和条件模拟，使情景能够针对特定历史危机时期（如全球金融危机、主权债务危机等）进行校准。
- 将生成的情景应用于基于压力测试弹性的模型，评估银行资本消耗，并识别尾部银行。

### 研究方法

论文采用三阶段方法：首先，利用非参数copula对日度金融指标进行自助抽样，生成金融变量路径；其次，构建金融压力指数（FSI），采用类似CISS的方法，通过指数加权移动平均（EWMA）估计时变相关性，并标准化指标；最后，将FSI作为外生变量纳入多国BVAR模型，该模型采用Minnesota型独立Normal-Inverted Wishart先验，误差项服从t分布，通过Metropolis-Hastings-Gibbs采样器估计，并利用卡尔曼滤波进行条件预测。

### 关键结果

生成的2008年型情景中，股市下跌幅度最大；2011年型情景中，主权利差上升最多；2022年型情景中，短期互换利率显著上升。；在银行压力测试中，2008年型情景对欧元区银行资本比率的负面影响最大，其次是2011年型情景。；2022年型情景对银行盈利能力有利，资本消耗较低。；2025年型情景（法国主权债务扰动）对系统级损失影响较小。；G-SIBs和投资银行在2008年型情景下受影响最大，而传统银行和全能银行在2011年型情景下受影响最大。

### 技术栈

- 非参数copula
- 自助抽样（bootstrap）
- 金融压力指数（FSI）
- 指数加权移动平均（EWMA）
- 贝叶斯向量自回归（BVAR）
- Minnesota先验
- Metropolis-Hastings-Gibbs采样器
- 卡尔曼滤波
- 压力测试弹性模型

### 方法优势

- 方法创新，结合多种统计和计量工具，生成大量内部一致的情景。
- 金融压力指数可分解，有助于理解情景驱动因素。
- BVAR模型考虑了厚尾分布，能捕捉极端事件。
- 实证应用展示了框架的实用性，并提供了对银行韧性的深入分析。

### 主要局限

- 情景生成依赖于历史数据，可能无法完全捕捉未来新型风险。
- BVAR模型设定可能受限于变量选择和先验设定。
- 压力测试弹性模型基于历史压力测试数据，可能无法完全反映当前银行资产负债表变化。
- 论文未提供所有情景的详细分布，仅展示了部分结果。

### 与当前研究方向的关联

论文与关键词高度相关，涉及宏观金融情景校准、压力测试、金融稳定、银行韧性、贝叶斯技术、金融copula等。

<details>
<summary><strong>发现与关联证据</strong></summary>

- **provider**：IDEAS/RePEc
- **series_url**：https://ideas.repec.org/s/ecb/ecbwps.html
- **free_download**：True
- **date_precision**：month

</details>

---

_知识库更新时间：2026-08-07T03:45:23.335275_
