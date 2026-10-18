---
title: "哪些文本重要：处理文本即数据回归中的模型不确定性，及其在央行沟通中的应用"
paper_id: "https://doi.org/10.48550/arxiv.2610.19720"
source: "openalex"
published: "2026-10-14T00:00:00"
score: 70.0
tags: ["paper", "banking-fiscal-monetary-policy", "Computational and Text Analysis Methods", "Statistical Methods and Inference", "Statistical Methods and Applications"]
---

# 哪些文本重要：处理文本即数据回归中的模型不确定性，及其在央行沟通中的应用

> **英文原标题**：Which Text Matters: Handling Model Uncertainty in Text-as-Data Regressions, with an Application to Central Bank Communication

[查看原文](https://arxiv.org/abs/2610.19720)

## 一句话结论

> 提出spike-and-slab广义可加模型联合选择文本协变量及其线性/非线性形式，应用于224场欧洲央行新闻发布会45个文本指标，发现仅稀疏指标能追踪专业通胀预期。

## 论文信息

- **作者**：Martin Feldkircher, Bernd Prostmaier, Paul Hofmarcher, Pierre Siklos
- **来源**：arXiv (Cornell University)
- **发布时间**：2026-10-14
- **相关度评分**：70.0
- **DOI**：[https://doi.org/10.48550/arxiv.2610.19720](https://doi.org/10.48550/arxiv.2610.19720)

## 相关性评分

- **商业银行**：0.0/10
- **货币政策**：7.0/10（最高匹配）
- **财政政策**：0.0/10

<details open>
<summary><strong>中文摘要</strong></summary>

社会科学家通常会将文本转换为协变量，如主题份额、理想点或情感得分，并将其纳入感兴趣的统计模型中。这种两步设计虽然便捷，但很少以理论为指导：几乎没有依据告诉分析者应该构建或纳入哪些基于文本的协变量。每种方法都体现了可争议的测量选择，而同一构念的竞争性操作化可能支持不同的结论，因此一个单一的研究问题就会产生一系列相互竞争的回归模型。哪些文本构建的协变量应纳入模型，以及以何种函数形式纳入，因而成为一个模型不确定性问题。我们提出钉板广义加性模型（spike-and-slab generalized additive models, SSGAMs），该模型能够联合选择协变量并确定其效应是线性的还是非线性的。我们以一个强大的非选举机构的沟通为例来说明该方法，考察来自2002年末至2025年中期224场欧洲中央银行月度新闻发布会的45个竞争性文本指标中，哪些能够追踪专业通胀预期。结果选中了一个稀疏的指标集合；广泛使用的替代指标以及所有测试的非线性效应均不携带增量信息。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Social scientists routinely convert text into covariates like topic shares, ideal points or sentiment scores, and insert them into statistical models of interest. This two-step design is convenient, but it is rarely guided by theory: little tells the analyst which text-based covariates to construct or include. Each approach embodies contestable measurement choices, and competing operationalizations of the same construct can support different conclusions, so a single research question gives rise to a menu of competing regression models. Which text constructed covariates belong in a model, and in what functional form, is thus a problem of model uncertainty. We propose spike-and-slab generalized additive models (SSGAMs), which jointly select covariates and determine whether their effects are linear or nonlinear. We illustrate the approach with the communication of a powerful unelected institution, asking which of 45 competing text indicators from 224 monthly European Central Bank press conferences, spanning late 2002 to mid-2025, track professional inflation expectations. A sparse set is selected; widely used alternatives, and every tested nonlinear effect, carry no incremental information.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

社会科学家常将文本转化为主题份额、理想点或情感得分等协变量，再放入统计模型。这种两步设计虽方便，但缺乏理论指导，研究者难以确定应构建或纳入哪些文本协变量。每种方法都包含有争议的测量选择，同一构念的不同操作化可能导致不同结论，因此一个研究问题会产生一系列竞争性回归模型。本文提出尖峰与平板广义可加模型（SSGAMs），联合选择协变量并判断其效应是线性还是非线性。以欧洲央行224场月度新闻发布会（2002年末至2025年中）的45个竞争性文本指标为例，考察哪些指标追踪专业通胀预期。结果选出一个稀疏集合；广泛使用的替代指标以及所有测试的非线性效应均不提供增量信息。

### 主要创新

- 将文本即数据回归中的测量多重性视为模型不确定性问题，并引入贝叶斯模型平均框架进行概率化处理。
- 提出使用尖峰与平板广义可加模型（SSGAMs），同时处理变量选择与函数形式选择两层不确定性。
- 将每个协变量的效应正交分解为线性部分与非线性偏离，使后验能够区分排除、线性纳入和非线性纳入三种状态。
- 在央行沟通应用中，系统性地比较45个竞争性文本指标，而非预先选择单一指标。
- 通过单指标设计与联合后验的对比，实证展示了指标预选择对结论的实质性影响。

### 研究方法

论文采用尖峰与平板广义可加模型（SSGAMs）。基础模型为可加模型，每个协变量的平滑函数用惩罚B样条基表示，并正交分解为严格线性部分与非线性偏离。选择通过参数扩展正态混合逆伽马（peNMIG）先验实现，对系数块方差施加尖峰与平板混合，尖峰因子为2.5×10^-4，平板方差先验为IG(5,25)，纳入权重先验为Beta(1,1)。使用R包spikeSlabGAM进行块吉布斯采样，运行5条平行链，每条10000次迭代，烧入5000次，稀疏间隔5，每条链保留1000个抽样，共5000个。收敛通过Gelman-Rubin潜在尺度缩减因子检验，阈值1.1。连续协变量在1%和99%分位数处缩尾。应用中将45个文本指标与 Consensus Economics 专业预测员一年期CPI通胀预测匹配，基线采用一个月领先（t+1）设定，并包含欧洲央行行长虚拟变量和危机期指示变量。

### 关键结果

对于预测水平，45个文本指标中仅两个通过纳入阈值（后验纳入概率>0.5）：来自脚本化介绍声明的Picault-Renault货币政策得分（P=0.841）和Syuzhet情感得分（P=0.660），二者均以线性形式进入。；Loughran-McDonald词典（P=0.029）、FinBERT（P=0.020）和Picault-Renault经济环境维度（P=0.034）被明确排除。；所有复杂性和可读性指标均未通过纳入阈值；Flesch-Kincaid年级水平的线性项P=0.033，非线性项P=0.315。；所有问答环节指标均未稳健入选；最接近的是总统回答中的类型-标记比（P=0.429）。；对于预测分歧，没有任何文本指标超过P=0.02，数据积极支持排除所有文本项。；单指标设计显示，六个指标中有五个在单独进入时获得5%水平显著，但联合后验表明其中两个的显著性源于与保留的Syuzhet得分强相关。；稳健性检验中，同期设定、非缩尾处理和加入滞后因变量后，主要选择结果基本不变；加入滞后因变量后，滞后项以P=1.00被选中并吸收0.95的解释变异，文本项不再存活。

### 技术栈

- 尖峰与平板广义可加模型（SSGAMs）
- 参数扩展正态混合逆伽马（peNMIG）先验
- 惩罚B样条基与正交分解
- 块吉布斯采样
- Gelman-Rubin潜在尺度缩减因子
- R包spikeSlabGAM
- Syuzhet词典
- Loughran-McDonald词典
- FinBERT变换器模型
- Picault-Renault欧洲央行词典
- Flesch阅读易读性、Flesch-Kincaid年级水平、ARI可读性指标
- 类型-标记比、复杂句比例、平均句长、平均词长、概念复杂性指数（CCI）

### 方法优势

- 方法上创新性地将变量选择与函数形式选择统一在一个贝叶斯后验框架中，克服了标准BMA强制线性的盲点。
- 应用问题具有高度现实意义，央行沟通的文本测量多重性问题突出，研究设计系统且全面。
- 通过单指标设计与联合后验的对比，直观展示了指标预选择如何导致不同结论，增强了方法论论证的说服力。
- 稳健性检验覆盖时间设定、缩尾处理和结果持续性三个维度，结果一致。
- 对零结果的报告具有方法论价值，能够区分“无证据”与“证据表明无效应”。

### 主要局限

- 模型假设扰动项独立，但两个结果均为持续性时间序列且使用重叠固定期限预测，纳入概率应视为描述性协变度量而非精确误差率检验。
- 候选集不包含宏观经济基本面，模型仅考察文本指标与专业预期的协变关系，不能识别因果效应。
- 预测分歧的代理指标（横截面标准差）仅为不完美代理。
- 样本中部分事件因转录解析不完整被排除，可能影响代表性。
- 非线性效应虽被检验但均未入选，无法排除其他函数形式或交互效应。

### 与当前研究方向的关联

论文与中央银行沟通、通胀预期和货币政策密切相关。它系统评估欧洲央行新闻发布会文本的哪些维度追踪专业通胀预期，直接涉及中央银行政策工具（沟通作为政策工具）和利率与通胀（通胀预期形成）。方法上处理文本即数据回归中的模型不确定性，对金融稳定和信用周期等关键词关联较弱，但为央行沟通研究提供了可推广的计量框架。

---

_知识库更新时间：2026-10-18T05:10:51.456469_
