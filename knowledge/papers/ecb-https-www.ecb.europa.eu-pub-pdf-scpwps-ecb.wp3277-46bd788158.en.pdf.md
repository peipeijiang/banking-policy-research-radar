---
title: "学习违约概率与压力测试"
paper_id: "ecb:https://www.ecb.europa.eu//pub/pdf/scpwps/ecb.wp3277~46bd788158.en.pdf"
source: "ecb"
published: "2026-08-24T09:00:00"
score: 80.0
tags: ["paper", "banking-fiscal-monetary-policy"]
---

# 学习违约概率与压力测试

> **英文原标题**：Learning probability of default and stress testing

[查看原文](https://www.ecb.europa.eu//pub/pdf/scpwps/ecb.wp3277~46bd788158.en.pdf)

## 一句话结论

> 该论文利用随机森林模型预测欧洲非金融企业违约概率，并应用于银行压力测试，通过银行-企业网络评估银行体系风险，主要贡献在于提高风险敏感性和识别尾部银行。

## 论文信息

- **作者**：-
- **来源**：ECB Working Papers
- **发布时间**：2026-08-24
- **相关度评分**：80.0
- **DOI**：-

## 相关性评分

- **商业银行**：8.0/10（最高匹配）
- **货币政策**：4.0/10
- **财政政策**：2.0/10

<details open>
<summary><strong>中文摘要</strong></summary>

我们利用随机森林（RF）分析欧洲非金融企业的违约概率（PD），并评估其对银行业压力测试的影响。为此，我们使用了企业财务报表（Orbis）和银行信贷登记（Anacredit）的数据。研究表明，在压力测试中，随机森林比逻辑回归展现出更强的风险敏感性，为情景严重程度对违约概率的非线性影响提供了新的视角。此外，我们展示了如何将基于随机森林的违约概率应用于银行与企业构成的网络中，通过贷款敞口这一关键传导渠道对银行业进行压力测试。通过对该网络生成的银行风险指标进行细致分析，进一步揭示了随机森林在捕捉非线性方面的优越性，这得益于其识别“尾部银行”的能力。我们的工作对中央银行及银行业监管机构均具有重要参考价值。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

We analyze the Probability of Default (PD) of non-financial corporations in Europe using Random Forests (RF) and assess implications for stress testing the banking sector. To this end, we exploit data on firms’ financial statements (Orbis) and banks’ credit registry (Anacredit). We show that RF displays stronger risk sensitivity than logistic regression in stress testing, shedding new light on the non-linear effect of scenario severity on PD. Moreover, we show how RF-based PD can be used in a network of banks and firms to stress test the banking sector through loan exposures as a key transmission channel of adverse scenarios. A granular inspection of banks’ riskiness indices derived from this network sheds light also on RF’s superior ability in capturing non-linearity thanks to its capability in identifying “tail banks”. Our work is relevant for central banks and banking supervisors alike.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

本文利用随机森林（RF）预测欧洲非金融企业的违约概率（PD），并评估其在银行部门压力测试中的应用。作者使用Orbis企业财务数据和Anacredit银行信贷登记数据，构建了企业层面的PD模型，并与逻辑回归（logit）进行对比。研究发现，RF在预测性能和风险敏感性方面均优于logit，尤其在压力测试中能捕捉非线性和异质性的冲击传导。此外，作者将RF预测的PD应用于银行-企业二分网络，通过贷款敞口传导压力情景，评估银行体系的稳健性。研究还发现，RF能识别“尾部银行”，凸显其捕捉非线性的能力。该研究为中央银行和银行监管者提供了基于机器学习的压力测试工具。

### 主要创新

- 将随机森林（RF）应用于企业违约概率预测，并系统评估其在压力测试中的优势。
- 利用SHAP值识别企业违约的关键驱动因素，并据此设计冲击传导机制。
- 构建银行-企业二分网络，将企业PD压力测试结果传导至银行体系，评估系统性风险。
- 通过情景严重性分析，揭示利率和GVA冲击对PD的非线性影响。
- 填补了机器学习在中央银行压力测试工具箱中的空白。

### 研究方法

本文采用随机森林（RF）算法预测企业违约概率，并与逻辑回归（logit）对比。数据来源为Orbis企业财务数据和Anacredit银行信贷登记数据。模型训练采用时间感知的组群划分，避免数据泄漏。通过SHAP值进行变量重要性分析。压力测试中，将宏观情景（如GVA增长、利率）映射到企业财务变量，利用弹性系数和资产负债表重构方法，模拟企业财务变化，进而预测压力情景下的PD。最后，将PD应用于银行-企业网络，计算银行风险指标。

### 关键结果

RF在样本内和样本外均优于logit，具体表现为：样本内MAE为0.006 vs 0.009，RMSE为0.005 vs 0.007，相关性差异为0.677 vs 0.257；样本外中位数MAE为0.0025 vs 0.0031，RMSE为0.0031 vs 0.0034，相关性差异为0.514 vs 0.359。在微观层面，RF的PR-AUC、ROC-AUC和校准性能均优于logit。压力测试中，RF对不利情景的敏感性更高，PD在首年翻倍，且能识别尾部银行。

### 技术栈

- 随机森林（Random Forests）
- 逻辑回归（Logistic Regression）
- SHAP（Shapley Additive Explanations）
- 弹性系数（Elasticities）
- 资产负债表重构（Balance sheet reconstruction）
- 二分网络（Bipartite network）
- 压力测试（Stress testing）

### 方法优势

- 1. 数据丰富，结合企业财务和银行信贷数据。2. 方法创新，将RF应用于压力测试，并展示其优势。3. 结果稳健，通过样本内外验证和多种指标对比。4. 政策相关性强，为监管机构提供新工具。5. 可解释性，利用SHAP增强模型透明度。

### 主要局限

- 1. 样本限制：仅包含10,000家企业，可能不具完全代表性。2. 数据质量：依赖Orbis数据，可能存在报告偏差。3. 模型简化：弹性系数和资产负债表重构方法较为简化，可能忽略复杂动态。4. 压力测试情景有限：仅基于EBA 2023情景，未考虑其他可能情景。5. 未考虑银行内生反应：银行可能调整贷款组合，但模型未模拟。

### 与当前研究方向的关联

本文与关键词高度相关：聚焦银行信贷风险（PD）、压力测试、金融稳定、宏观审慎政策，并采用机器学习方法（随机森林），符合研究背景中对银行信贷与风险承担、金融稳定和信用周期的关注。

---

_知识库更新时间：2026-08-26T02:23:25.598187_
