---
title: "通胀解构：利用神经菲利普斯曲线解析关键组成部分"
paper_id: "https://doi.org/10.22004/ag.econ.406292"
source: "openalex"
published: "2026-08-07T00:00:00"
score: 80.0
tags: ["paper", "banking-fiscal-monetary-policy", "Monetary Policy and Economic Impact", "Stock Market Forecasting Methods", "Global Financial Crisis and Policies"]
---

# 通胀解构：利用神经菲利普斯曲线解析关键组成部分

> **英文原标题**：Inflation Unpacked: Breaking Down the Key Components Using a Neural Phillips Curve

[查看原文](https://doi.org/10.22004/ag.econ.406292)

## 一句话结论

> 该研究使用半球神经网络（HNN）在菲律宾新凯恩斯菲利普斯曲线框架下分解通胀的驱动因素，为货币政策提供可解释的指标。

## 论文信息

- **作者**：Joan Christine S. Allon-Pineda
- **来源**：AgEcon Search (University of Minnesota, USA)
- **发布时间**：2026-08-07
- **相关度评分**：80.0
- **DOI**：[https://doi.org/10.22004/ag.econ.406292](https://doi.org/10.22004/ag.econ.406292)

## 相关性评分

- **商业银行**：0.0/10
- **货币政策**：8.0/10（最高匹配）
- **财政政策**：0.0/10

<details open>
<summary><strong>中文摘要</strong></summary>

背景与目标：有效的货币政策制定需要清晰理解通胀的潜在驱动因素。对于菲律宾中央银行（Bangko Sentral ng Pilipinas, BSP）等央行而言，这一任务颇具挑战性，因为通胀反映了需求侧压力、供给侧冲击与预期之间的相互作用。通胀动态的关键组成部分，包括产出缺口和通胀预期，均属于不可观测变量，往往难以精确度量。传统的菲利普斯曲线模型通常依赖较强的假设、滤波方法或基于调查的代理变量，这些方法可能对设定偏误、测量误差和非线性特征较为敏感。本研究采用深度学习方法，考察菲律宾的通胀动态，并在新凯恩斯菲利普斯曲线框架下，分离实际经济活动、通胀预期和大宗商品价格对通胀的贡献。

方法论：本研究采用半球神经网络（Hemisphere Neural Network, HNN），这是一种深度神经网络架构，通过将输入变量分组到不同的“半球”来提高模型的可解释性。每个半球对应通胀的一个关键组成部分：实际经济活动、通胀预期和大宗商品价格。该结构使模型能够提取可被解释为宏观经济状态的潜在指标，并将实际通胀分解为各组成部分的贡献。与通常作为“黑箱”运行的标准神经网络不同，HNN在最终层施加了具有经济含义的结构，使估计的组成部分更加透明。模型使用菲律宾季度宏观经济数据进行估计，并基于其生成有意义的通胀预测、与历史宏观经济事件的一致性，以及产出缺口和通胀预期的可解释指标来评估其表现。

主要发现：结果表明，菲律宾通胀可分解为实际经济活动、通胀预期和大宗商品价格的各自贡献。长期通胀预期在样本期内保持相对稳定，约为3.5%–4.5%，与BSP的2%–4%通胀目标区间基本一致。这种稳定性表明预期仍相对较好地锚定。大宗商品价格解释了通胀中的大部分短期波动，尤其是在2014–2015年石油供应过剩和2021–2022年全球供应链中断等时期。相比之下，实际经济活动在中期通胀变动中发挥更为重要的作用，特别是在疫情期间和疫情后复苏阶段。结果还表明，菲律宾通胀与经济活动之间的关系仍然显著，这与部分文献中关于菲利普斯曲线已弱化或消失的观点相反。HNN推导出的实际经济活动缺口大致反映了国内经济状况，可被解释为衡量通胀压力的补充指标。同样，基于模型的通胀预期度量与企业和专业预测机构的短期至中期预期相吻合，表明在基于调查的指标有限时，该度量可作为有用的补充指标。

政策启示：研究结果凸显了可解释深度学习方法在货币政策分析中的实用性。通过区分需求侧压力驱动的通胀与暂时性供给冲击引发的通胀，HNN可帮助政策制定者评估通胀变动是否需要收紧货币政策、放松货币政策或采取更为谨慎的政策应对。由实际经济活动或预期驱动的通胀可能需要更强的货币政策回应，而主要由暂时性大宗商品价格冲击导致的通胀则可能支持更为审慎的政策取向。模型对产出缺口和通胀预期的估计还可补充BSP用于评估国内需求状况、预期形成机制以及通胀目标可信度的现有指标。总体而言，本研究表明，理论引导的机器学习可以加强宏观经济监测，并支持更具针对性、基于证据的货币政策决策。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Background and Objectives: Effective monetary policymaking requires a clear understanding of the underlying drivers of inflation. For central banks such as the Bangko Sentral ng Pilipinas (BSP), this task is challenging because inflation reflects the interaction of demand-side pressures, supply-side shocks, and expectations. Key components of inflation dynamics, including the output gap and inflation expectations, are unobserved and are often difficult to measure accurately. Traditional Phillips curve models typically rely on strong assumptions, filtering methods, or survey-based proxies, which may be sensitive to misspecification, measurement error, and nonlinearities. This study applies a deep learning approach to examine inflation dynamics in the Philippines and disentangle the contributions of real activity, inflation expectations, and commodity prices within a New Keynesian Phillips Curve framework.Methodology: The study employs a Hemisphere Neural Network (HNN), a deep neural network architecture designed to improve interpretability by grouping input variables into separate “hemispheres.” Each hemisphere corresponds to a key component of inflation: real activity, inflation expectations, and commodity prices. This structure allows the model to extract latent indicators that can be interpreted as macroeconomic states and to decompose realized inflation into component-specific contributions. Unlike standard neural networks, which often operate as black boxes, the HNN imposes an economically meaningful structure on the final layer, making the estimated components more transparent. The model is estimated using Philippine quarterly macroeconomic data and is assessed based on its ability to generate meaningful inflation forecasts, align with historical macroeconomic events, and produce interpretable indicators of the output gap and inflation expectations.Key Findings: The results show that Philippine inflation can be decomposed into distinct contributions from real activity, inflation expectations, and commodity prices. Long-run inflation expectations remained relatively stable at around 3.5–4.5 percent over the sample period, broadly consistent with the BSP’s inflation target range of 2–4 percent. This stability suggests that expectations have remained relatively well anchored. Commodity prices account for much of the short-term volatility in inflation, particularly during episodes such as the 2014–2015 oil supply glut and the 2021–2022 global supply chain disruptions. By contrast, real activity appears to play a more important role in medium-term inflation movements, especially during the pandemic and post-pandemic recovery periods. The results also indicate that the relationship between inflation and economic activity in the Philippines remains relevant, contrary to claims in some strands of the literature that the Phillips curve has weakened or disappeared. The HNN-derived real activity gap broadly reflects domestic economic conditions and can be interpreted as an additional measure of inflationary pressure. Similarly, the model-based measure of inflation expectations aligns with short- to medium-term expectations from businesses and professional forecasters, suggesting that it can serve as a useful supplementary indicator when survey-based measures are limited.Policy Implications: The findings highlight the usefulness of interpretable deep learning methods for monetary policy analysis. By distinguishing between inflation driven by demand-side pressures and inflation arising from temporary supply shocks, the HNN can help policymakers assess whether inflation movements warrant monetary tightening, easing, or a more cautious policy response. Inflation driven by real activity or expectations may call for a stronger monetary policy response, while inflation caused mainly by temporary commodity price shocks may justify a more measured approach. The model’s estimates of the output gap and inflation expectations can also complement existing indicators used by the BSP to assess domestic demand conditions, expectation formation, and the credibility of the inflation target. Overall, the study demonstrates that theory-guided machine learning can strengthen macroeconomic monitoring and support more targeted, evidence-based monetary policy decisions.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

本研究采用半球神经网络（HNN）方法，在新凯恩斯菲利普斯曲线框架下分解菲律宾通胀的驱动因素。模型将输入变量分为实际经济活动、通胀预期和商品价格三个半球，提取潜在因子并分解通胀贡献。结果显示，长期通胀预期稳定在3.5-4.5%，商品价格解释了大部分短期波动，实际经济活动在疫情期间及之后贡献显著。HNN估计的产出缺口与现有指标相关，通胀预期与调查指标一致。研究认为菲利普斯曲线在菲律宾仍然有效，HNN有助于区分需求拉动和供给推动的通胀，为货币政策提供参考。

### 主要创新

- 将半球神经网络（HNN）应用于菲律宾通胀分解，提高模型可解释性。
- 在NKPC框架下同时分解实际经济活动、通胀预期和商品价格三个成分。
- 提取可解释的产出缺口和通胀预期指标，与现有指标对比验证。
- 证明菲利普斯曲线在菲律宾仍然有效，反驳其弱化或消失的观点。

### 研究方法

采用半球神经网络（HNN），将输入变量分组为三个半球，每个半球通过全连接网络提取潜在因子，最终输出为各半球贡献之和。模型使用PyTorch实现，包含三个隐藏层（400神经元）用于因子提取，三个隐藏层（100神经元）用于时变系数，ReLU激活，Adam优化器，学习率0.05，最大100轮，早停和dropout（0.2）防止过拟合，采用300次块自助法估计不确定性。

### 关键结果

长期通胀预期稳定在3.5-4.5%，符合BSP目标区间。；商品价格解释了大部分短期通胀波动，如2014-2015年石油供应过剩和2021-2022年供应链中断。；实际经济活动在疫情期间及之后对通胀贡献显著。；HNN产出缺口与现有指标相关性较高（如与滤波法相关系数0.683）。；HNN通胀预期与商业预期调查当前季度和下一季度预测相关性高（0.846和0.844）。

### 技术栈

- 半球神经网络（HNN）
- PyTorch
- ReLU激活函数
- Adam优化器
- 早停法
- Dropout
- 块自助法（block bootstrap）

### 方法优势

- 模型结构具有经济理论支撑，可解释性强。
- 能够分解通胀成分，区分需求拉动和供给推动因素。
- 提取的产出缺口和通胀预期与现有指标一致，具有实用性。
- 采用多种正则化技术，降低过拟合风险。

### 主要局限

- 样本量相对较小（106个季度观测），可能影响模型稳定性。
- 模型假设各成分独立，可能忽略交互作用。
- HNN产出缺口与现有指标存在差异，解释需谨慎。
- 未考虑货币政策、金融条件等额外因素。

### 与当前研究方向的关联

论文与关键词高度相关，涉及货币政策、通胀、菲利普斯曲线、神经网络、产出缺口、通胀预期等核心概念，为货币政策分析提供了新工具。

---

_知识库更新时间：2026-08-09T02:41:08.181144_
