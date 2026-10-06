---
title: "欧洲央行货币政策向单边欧元化经济体的传导"
paper_id: "ecb:https://www.ecb.europa.eu//pub/pdf/scpwps/ecb.wp3293~a7c6243bcc.en.pdf"
source: "ecb"
published: "2026-10-05T09:00:00"
score: 85.0
tags: ["paper", "banking-fiscal-monetary-policy"]
---

# 欧洲央行货币政策向单边欧元化经济体的传导

> **英文原标题**：ECB monetary policy transmission to unilaterally euroised economies

[查看原文](https://www.ecb.europa.eu//pub/pdf/scpwps/ecb.wp3293~a7c6243bcc.en.pdf)

## 一句话结论

> 论文利用结构VAR模型研究欧元区货币政策冲击对单边欧元化经济体（黑山和科索沃）产出和通胀的溢出效应，发现存在显著但滞后的影响，且对商业周期波动的贡献有限。

## 论文信息

- **作者**：-
- **来源**：ECB Working Papers
- **发布时间**：2026-10-05
- **相关度评分**：85.0
- **DOI**：-

## 相关性评分

- **商业银行**：0.0/10
- **货币政策**：8.5/10（最高匹配）
- **财政政策**：0.0/10

<details open>
<summary><strong>中文摘要</strong></summary>

利用单边欧元化的独特背景，本文考察了欧元区货币政策对黑山和科索沃的溢出效应。通过一个带有块外生性的结构向量自回归（VAR）模型，研究表明欧元区货币政策冲击能够显著影响这些经济体的产出和通胀，尽管响应存在滞后，同时对其整体商业周期波动的贡献较为有限。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Leveraging the unique setting of unilateral euroisation, this paper examines the spillover effects of euro area monetary policy on Montenegro and Kosovo. Through the lens of a structural VAR model with block exogeneity, it shows that euro area monetary policy shocks can significantly influence output and inflation in these economies, albeit with a delayed response, while contributing only modestly to their overall business cycle fluctuations.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

本文利用黑山和科索沃单边欧元化的独特背景，研究欧元区货币政策对这两个经济体的溢出效应。作者采用带有块外生性约束的结构向量自回归模型（SVARX），使用2006Q1至2024Q3的季度数据，识别欧洲央行货币政策冲击对黑山和科索沃产出与通胀的影响。研究发现，欧元区货币政策冲击会显著影响这两个经济体的产出和通胀，但效应存在延迟，峰值出现在冲击后2至4年；同时，这些冲击对两国商业周期波动的贡献有限，五年期预测误差方差分解中占比不超过7%。这表明国内政策在稳定经济中发挥更重要作用。

### 主要创新

- 首次系统性地记录单边欧元化经济体货币政策传导的“第二段”，即从欧洲央行政策到实际产出和价格。
- 利用黑山和科索沃无法影响欧洲央行决策的外生性，减少识别货币政策溢出效应时的混淆因素。
- 将块外生性SVAR方法应用于欧洲单边欧元化背景，区别于美洲美元化经济体的研究。
- 结合递归Cholesky分解与块外生性约束，识别欧元区货币政策冲击对小型开放经济体的动态影响。
- 提供历史分解证据，评估2022-23年欧洲央行紧缩周期对黑山和科索沃的滞后影响。

### 研究方法

论文采用结构向量自回归模型 with 块外生性（SVARX），包含五个变量：欧元区产出、欧元区通胀、欧元区利率（三个月Euribor）、国内产出和国内通胀。通过块外生性约束，确保欧元区变量不受国内变量反馈影响。使用递归Cholesky分解识别货币政策冲击，假设欧洲央行 contemporaneously 对欧元区产出和通胀做出反应，而其他宏观总量滞后反应。模型使用贝叶斯技术估计，采用独立Normal-Wishart先验，滞后阶数为4（基于AIC），并通过BEAR工具箱实现块外生性约束。数据为季度数据，2006Q1至2024Q3，欧元区数据来自Eurostat，黑山和科索沃数据来自MONSTAT、科索沃统计局和IMF WEO。

### 关键结果

一个标准差的欧洲央行政策利率收缩性冲击（约30个基点）导致黑山和科索沃产出和通胀下降。；产出峰值下降约0.5个百分点，通胀下降约0.2至0.3个百分点，效应在2年后显现，持续2至4年。；欧元区货币政策冲击对国内产出和通胀波动的贡献有限，五年期预测误差方差分解中占比不超过7%。；历史分解显示，2022-23年欧洲央行紧缩对黑山和科索沃的产出和通胀在2024年开始产生抑制效应。；结果对替代递归排序和滞后阶数选择具有定性稳健性。

### 技术栈

- 结构向量自回归模型（SVAR）
- 块外生性约束（block exogeneity restrictions）
- 递归Cholesky分解
- 贝叶斯估计方法
- 独立Normal-Wishart先验
- BEAR工具箱
- 脉冲响应函数（IRFs）
- 预测误差方差分解（FEVD）
- 历史分解
- Akaike信息准则（AIC）
- Augmented Dickey-Fuller（ADF）和KPSS检验

### 方法优势

- 利用单边欧元化的独特制度背景，提供识别货币政策外生冲击的自然实验。
- 块外生性假设合理，符合欧元区与小型欧元化经济体之间的非对称关系。
- 结合多种稳健性检验，包括替代递归排序、不同滞后阶数和缩短样本，增强结果可信度。
- 研究问题具有明确政策含义，为黑山和科索沃的国内政策制定提供参考。
- 方法上遵循经典文献，如Cushman and Zha (1997)和Willems (2013)，具有学术延续性。

### 主要局限

- 科索沃季度国民账户数据从2011Q1才开始，2006-2010年数据通过线性插值扩展，可能引入人为平滑。
- 样本期相对较短，尤其对科索沃而言，可能影响估计精度。
- 模型仅包含五个变量，可能遗漏其他重要传导渠道或冲击。
- 单边欧元化经济体的结构特征可能随时间变化，模型假设参数稳定。
- 论文未详细讨论银行信贷渠道的具体作用，尽管提及银行部门由欧元区母行主导。

### 与当前研究方向的关联

论文与货币政策传导、中央银行政策工具、利率与通胀、金融稳定等关键词高度相关。研究聚焦欧洲央行货币政策对单边欧元化经济体的溢出效应，涉及货币政策国际传导、利率冲击对产出和通胀的影响，以及国内政策在稳定经济中的作用。同时，论文提及银行部门由欧元区母行主导，间接关联银行信贷渠道和金融中介。但论文未直接涉及财政政策、公共债务、量化宽松或宏观审慎政策的具体分析，因此与这些关键词的相关性较低。

---

_知识库更新时间：2026-10-06T06:54:16.531805_
