---
title: "Deep-π*：趋势通胀的神经网络估计"
paper_id: "ecb:https://www.ecb.europa.eu//pub/pdf/scpwps/ecb.wp3307~d3d2e0c5e4.en.pdf"
source: "ecb"
published: "2026-11-04T10:00:00"
score: 75.0
tags: ["paper", "banking-fiscal-monetary-policy"]
---

# Deep-π*：趋势通胀的神经网络估计

> **英文原标题**：Deep-π*: a neural network estimate of trend inflation

[查看原文](https://www.ecb.europa.eu//pub/pdf/scpwps/ecb.wp3307~d3d2e0c5e4.en.pdf)

## 一句话结论

> 论文用神经网络将趋势通胀的冲击建模为大量宏观指标的（非线性）函数，并用Shapley值归因趋势变动，发现疫情后美国当前趋势通胀主要由就业变量驱动、前瞻趋势通胀更早上升且预测更准。

## 论文信息

- **作者**：-
- **来源**：ECB Working Papers
- **发布时间**：2026-11-04
- **相关度评分**：75.0
- **DOI**：-

## 相关性评分

- **商业银行**：1.0/10
- **货币政策**：7.5/10（最高匹配）
- **财政政策**：0.5/10

<details open>
<summary><strong>中文摘要</strong></summary>

大多数趋势通胀的经验模型将其视为由未观测冲击驱动的潜在随机游走，因此无法说明哪些经济状况会推动其变化。Deep-π* 将趋势的 innovations 设定为大量宏观经济指标的可能非线性函数，并用神经网络进行估计，从而可以使用 Shapley 值将趋势的每一次变动归因于其背后的指标。两个互补的损失函数定义了当前趋势（拟合当前通胀）和前瞻性趋势（最好地预测未来一年的通胀）。在美国数据中，与就业相关的变量是疫情后当前趋势上升的最大贡献者。然而，前瞻性趋势上升得更早，从疫情开始起，实际活动、就业以及货币和信贷就是主要驱动因素，并且比当前趋势提前八到十二个月达到峰值。两种趋势都看穿了能源和大宗商品价格的大部分变动。指标的贡献是非线性的，并且它们之间存在相当大的交互作用。在通胀飙升期间每月重新估计，该模型对通胀的预测比标准 UC-SV 模型和随机游走更准确；并且在2021年初，当专业预测者预计通胀为3%或更低时，前瞻性趋势已经发出持续通胀上升的信号。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Most empirical models of trend inflation treat it as a latent random walk driven by unobserved shocks, so they cannot say which economic conditions move it. Deep- π*makes the innovations to the trend a possibly nonlinear function of a large number of macroeconomic indicators, estimated with neural networks, so that Shapley values can be used to attribute every movement of the trend to the indicators behind it. Two complementary loss functions define a current trend, which fits inflation today, and a forward-looking trend, which best predicts inflation over the next year. In US data, employment-related variables were the largest contributors to the post-pandemic rise of the current trend. However, the forwardlooking trend rose earlier, with real activity, employment, and money and credit as the main drivers from the start of the pandemic, and peaked eight to twelve months before the current trend. Both trends looked through most of the movements in energy and commodity prices. The contributions of the indicators are nonlinear, with sizeable interactions between them. Re-estimated every month during the surge, the model forecast inflation more accurately than the standard UC-SV model and a random walk, and in early 2021, when professional forecasters expected inflation of 3% or less, the forward-looking trend was already signalling an increase in persistent inflation.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

论文提出Deep-π*模型，将趋势通胀的 innovations 设为大量宏观经济指标的可能非线性函数，并用神经网络估计，从而可用Shapley值将趋势的每次变动归因于背后的指标。模型定义两种互补损失函数：计量经济学家损失（拟合当前通胀）得到当前趋势，央行行长损失（最优预测未来一年通胀）得到前瞻性趋势。基于美国1970-2025年122个FRED-MD指标，模型识别了美国通胀历史主要阶段；疫情后当前趋势上升至6.7%-7.5%，劳动力市场是当前趋势上升的最大贡献者（41%-52%），而前瞻性趋势更早上升，主要受实际活动、就业及货币信贷驱动，并提前8-12个月见顶。模型在实时预测中优于UC-SV和随机游走，2021年初前瞻性趋势已预示持续通胀上升。

### 主要创新

- 将趋势通胀的 innovations 建模为大量宏观经济指标的可能非线性函数，用神经网络估计，使趋势变动可归因于可观测经济条件，而非不可解释的随机冲击。
- 提出两种损失函数（计量经济学家损失和央行行长损失），分别定义当前趋势和前瞻性趋势，明确区分“解释当前通胀的持续成分”与“最优预测未来通胀的趋势”。
- 设计简约的基于相似性的因果注意力机制，仅增加三个参数，即可让趋势利用指标的历史信息而不固定滞后阶数。
- 将波动率状态纳入与趋势相同的递归结构，由第二个小型网络驱动，保持似然闭式可解，同时具备随机波动率的持续性和GARCH式的数据驱动特征。
- 利用分组Shapley值对趋势 innovations 进行精确分解，并因趋势对 innovations 线性而将贡献传递至趋势水平，实现逐月精确归因。

### 研究方法

模型将通胀建模为自回归过程，其长期水平为持续趋势；趋势递归为 π*_t = θπ*_{t-1} + (1-θ)τ_t，其中 innovation τ_t 是宏观经济指标向量的可能非线性函数，经 tanh 变换有界。采用四种神经网络架构：编码器（逐层压缩指标至标量）或相似性因果注意力加编码器；误差尺度为常数或时变波动率状态（由第二网络驱动）。使用两种损失函数估计：计量经济学家损失为当前通胀的Student-t负对数似然；央行行长损失为未来12个月通胀预测的负对数预测密度。趋势不确定性用Monte Carlo dropout和不同初始化的网络集成度量。使用分组Shapley值进行精确归因。样本为美国1970年2月至2025年12月CPI通胀和122个FRED-MD指标，并进行实时重估计评估。

### 关键结果

八种估计在美國通胀历史主要阶段上一致：1979-80年趋势峰值约13%，大缓和期平均约3%，2010年代约2%，疫情后升至6.7%-7.5%，为1981年以来最高。；前瞻性趋势在2021年3月见顶，比当前趋势早8-12个月，比通胀本身早一年以上。；当前趋势的上升主要由劳动力市场驱动，从2019年1月至峰值，就业贡献41%-52%；工资就业和职位空缺指数在两种架构中均增加上升。；前瞻性趋势自疫情开始上升，编码器架构主要归因于实际活动和就业，注意力架构主要归因于2020年货币和信贷激增。；价格（包括能源和商品价格）贡献很小，在趋势上升的4.9-5.6个百分点中最多贡献0.7个百分点，趋势看穿了大部分供给冲击相关的价格变动。；指标贡献明显非线性：九个组中八个组，其自身指标的线性函数无法复现其贡献变动的16%-40%（编码器）和最高53%（注意力架构）。；实时评估中，模型预测比UC-SV和随机游走更准确，与自回归相当；前瞻性趋势给出最准确的一年期密度预测。2021年初SPF预期未来一年通胀2.0%，前瞻性趋势已指向近4%，实际为7.3%。

### 技术栈

- 前馈神经网络（多层感知机）编码器，SiLU/Swish激活函数，逐层宽度减半
- 基于余弦相似性和几何衰减的因果注意力机制
- Student-t分布负对数似然（计量经济学家损失）
- 负对数预测密度（央行行长损失）
- Monte Carlo dropout和网络集成用于不确定性度量
- 分组Shapley值（groupShapley）精确归因
- 时变波动率状态递归，由第二神经网络驱动
- 梯度下降估计，似然闭式可解
- FRED-MD数据库122个宏观经济指标

### 方法优势

- 创新性地将神经网络嵌入趋势-周期分解，使趋势变动可归因于可观测经济条件，兼顾灵活性与经济解释性。
- 两种损失函数明确区分当前趋势与前瞻性趋势，回应政策制定中对中期通胀判断的需求。
- 注意力机制简约（仅三个参数），适合宏观经济学短样本，且权重具有直接可读性。
- 分组Shapley值提供精确、可加的逐月归因，因趋势对 innovations 线性而可传递至趋势水平。
- 实时评估设计严谨，与UC-SV、随机游走、自回归和SPF预测进行比较，并报告密度预测准确性。
- 波动率状态保持似然闭式可解，避免粒子滤波或Kalman滤波的计算负担。

### 主要局限

- 两种架构对前瞻性趋势上升的归因不同（编码器侧重实际活动和就业，注意力架构侧重货币信贷），作者将其解读为模型不确定性，但未提供明确的选择标准。
- 指标组并非结构性冲击，例如就业同时反映劳动供给和需求，因此归因不能直接解释为因果效应。
- 模型仅应用于美国数据，对其他经济体（如欧元区）的适用性尚未验证。
- 实时评估中模型对通胀下降的预判不如专业预测者，趋势仅在月度通胀下降后才实时回落。
- 注意力机制虽简约，但其相似性权重和衰减参数的经济含义仍需进一步检验。
- 趋势的初始条件和网络参数估计可能影响样本早期结果，但论文未详细讨论其敏感性。

### 与当前研究方向的关联

论文与利率与通胀、中央银行政策工具、货币政策密切相关：趋势通胀的估计是货币政策中期决策的核心，两种损失函数直接对应央行关注的中期通胀预测。与金融稳定和信用周期的关联体现在货币信贷指标对前瞻性趋势的贡献，以及波动率状态对通胀不确定性的刻画。与财政政策、银行信贷与风险承担、资本和流动性监管、量化宽松、公共债务等关键词的直接关联较弱，但模型框架可扩展至其他缓慢移动变量（如潜在产出增长或自然利率），对货币政策与金融稳定分析具有间接参考价值。

---

_知识库更新时间：2026-11-05T07:20:55.788246_
