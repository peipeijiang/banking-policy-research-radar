---
title: "估计国债需求与供给变化对收益率的影响"
paper_id: "federal_reserve:https://www.federalreserve.gov/econres/ifdp/estimating-yield-impacts-of-treasury-demand-and-supply-changes.htm"
source: "federal_reserve"
published: "2026-09-18T12:45:00"
score: 65.0
tags: ["paper", "banking-fiscal-monetary-policy"]
---

# 估计国债需求与供给变化对收益率的影响

> **英文原标题**：IFDP Paper: Estimating Yield Impacts of Treasury Demand and Supply Changes

[查看原文](https://www.federalreserve.gov/econres/ifdp/estimating-yield-impacts-of-treasury-demand-and-supply-changes.htm)

## 一句话结论

> 论文构建时变需求系统，利用工具变量估计美国国债分部门需求弹性，发现国债市场对价格日益敏感，当前每增加1000亿美元供给约推高5年期收益率3个基点，并可用于评估美联储资产负债表政策等情景。

## 论文信息

- **作者**：-
- **来源**：Federal Reserve FEDS and IFDP
- **发布时间**：2026-09-18
- **相关度评分**：65.0
- **DOI**：-

## 相关性评分

- **商业银行**：1.0/10
- **货币政策**：6.5/10（最高匹配）
- **财政政策**：5.0/10

<details open>
<summary><strong>中文摘要</strong></summary>

Daniel Beltran和Canlin Li我们构建了一个丰富的需求系统框架，以量化美国国债（U.S. Treasury）供需变化对收益率的影响。我们的模型捕捉了随时间变化的持有份额，并使用工具变量估计了各部门的需求弹性。我们发现，随着价格敏感度较低的外国官方投资者参与度下降，以及价格敏感度较高的对冲基金和其他私人投资者作用上升，国债市场随时间推移变得日益价格敏感。目前，国债供给增加1000亿美元会使五年期收益率上升约3个基点。我们通过表明投资者基础的变化能够解释历史收益率变化的显著部分，验证了该模型。我们的框架为政策分析和反事实情景提供了一个灵活的工具，包括外国官方投资者抛售以及美联储（Federal Reserve）资产负债表政策的收益率效应。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Daniel Beltran and Canlin Li We develop a rich demand system framework to quantify the yield effects of shifts in U.S. Treasury supply and demand. Our model captures time-varying holdings shares and estimates sectoral demand elasticities using instrumental variables. We find that the Treasury market has become increasingly price-sensitive over time, driven by the declining participation of less price-sensitive foreign official investors and the rising role of more price-sensitive hedge funds and other private investors. A $100 billion increase in Treasury supply currently raises five-year yields by approximately 3 basis points. We validate the model by showing that the shifts in investor base explain a significant portion of historical yield changes. Our framework provides a flexible tool for policy analysis and counterfactual scenarios, including the yield effects of foreign official investor sales and Federal Reserve balance sheet policies.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

本文构建了一个丰富的需求系统框架，量化美国国债供给与需求变动对收益率的影响。模型捕捉时变持有份额，并使用工具变量估计各投资者部门的需求弹性。研究发现，国债市场随时间变得越来越价格敏感，原因在于价格敏感度较低的外国官方投资者参与度下降，而价格敏感度较高的对冲基金和其他私人投资者作用上升。当前国债供给增加1000亿美元大约使五年期收益率上升3个基点。作者通过表明投资者基础变化能解释历史收益率变化的显著部分来验证模型。该框架为政策分析和反事实情景提供了灵活工具，包括外国官方投资者抛售和美联储资产负债表政策的收益率效应。

### 主要创新

- 构建了一个综合需求系统，使用贝叶斯动态线性模型（DLM）估计投资者部门的时变持有份额，并施加份额加总为1的约束，确保内部一致性。
- 在国债需求弹性估计中，使用两阶段最小二乘法（2SLS）并针对不同投资者类型选择特定控制变量，以解决内生性和工具变量强度问题，发现部门间价格敏感度存在显著异质性。
- 将国债分为短期国库券和长期国债两个不同资产类别处理，因为短期国库券无利率久期风险，主要用于现金管理，而长期国债具有久期风险。
- 通过将历史收益率变化分解为标准收益率曲线因子和投资者基础变化的贡献，验证了模型，表明投资者基础与收益率之间的估计关系能解释历史收益率变动的显著部分。
- 提供了灵活的政策分析工具，可量化外国官方投资者抛售和美联储资产负债表政策等反事实情景的收益率效应。

### 研究方法

论文首先定义部门收益率弹性β_i = d ln H_i / dy，并推导市场总弹性β_M = Σ ω_i β_i，以及市场乘数dy/(dS/S) = 1/β_M。理论框架遵循Koijen and Yogo (2019)的需求系统方法，假设投资者在风险-收益权衡下解决投资组合选择问题，得到对数需求函数。数据来自美联储金融账户（Z.1表）和财政部国际资本（TIC）系统，涵盖25个投资者部门，并合并为18个部门。使用贝叶斯动态线性模型（DLM）估计时变持有份额，状态方程为随机游走，观测方程将持有量与未偿量通过持有份额联系起来，并施加加总约束。对于13个部门，使用2SLS估计国债需求对收益率的半弹性，样本为2009Q1至2022Q1（排除2020Q1）。工具变量为美联储、政府支持企业、州和地方政府及其他价格不敏感部门持有的国债份额。第一阶段回归收益率对工具变量和控制变量，第二阶段使用预测收益率。控制变量包括滞后持有份额、美元指数、VIX、企业利润率、TED利差、布伦特原油价格、标普500指数和CPI通胀等，通过选择使弹性t统计量绝对值最大化的控制变量组合。

### 关键结果

国债市场随时间变得越来越价格敏感，主要由于投资者基础的结构性变化：价格敏感度较低的外国官方投资者参与度下降，而价格敏感度较高的对冲基金和其他私人投资者作用上升。；当前国债供给增加1000亿美元大约使五年期收益率上升3个基点；若以占未偿国债1%的供给增加衡量，当前收益率效应约为8个基点。；部门需求弹性存在显著异质性：家庭和对冲基金（HHF）弹性约为41，经纪交易商约为12，ABS发行人、ETF和外国私人投资者约为10，财产意外险、共同基金和非金融企业约为5至8，外国官方投资者、养老金和寿险公司弹性较低（约2至3），银行弹性为负（约-6）。；在正常时期，高弹性投资者的存在会抑制供给或需求冲击对收益率的影响；但在压力时期，若这些投资者退出市场，市场弹性会突然降低，放大冲击对收益率的影响。；假设外国官方投资者抛售5000亿美元国债，在当前市场条件下收益率约上升14个基点；若家庭和对冲基金抛售5000亿美元，由于市场弹性降低，收益率约上升55个基点。；在美联储资产负债表缩减至GDP的5%并持续净发行的情景下，美联储缩表累计贡献约50个基点的收益率上升，净发行再贡献约62个基点，总计约112个基点。

### 技术栈

- 贝叶斯动态线性模型（DLM）
- 卡尔曼滤波和平滑
- 两阶段最小二乘法（2SLS）
- 工具变量法
- HAC（Newey-West）标准误
- Wu-Hausman内生性检验
- 第一阶段F统计量弱工具变量检验
- 交叉验证LASSO（作为稳健性检验）

### 方法优势

- 构建了时变持有份额的需求系统，能够捕捉投资者基础随时间的动态变化，比假设恒定份额或使用历史平均份额的方法更贴近现实。
- 针对不同投资者类型使用特定控制变量和2SLS估计，解决了部门间需求冲击异质性和工具变量强度问题，提高了弹性估计的可靠性。
- 将国债分为短期国库券和长期国债两个资产类别，更准确地反映了不同投资者的持有动机和风险特征。
- 通过分解历史收益率变化验证模型，表明投资者基础变化能解释收益率变动的显著部分，增强了模型的可信度。
- 提供了灵活的政策分析工具，能够量化多种反事实情景的收益率效应，具有明确的政策含义。

### 主要局限

- 论文承认其需求系统方法建立在Koijen and Yogo (2019)基础上，估计资产需求弹性时没有完全指定投资者对全部资产收益的结构性信念模型。
- Fuchs et al. (2025)表明，在这种情况下，估计的需求弹性通常会被一个不可观测的“潜在映射”污染，该映射将风险收益偏好与观测到的资产头寸联系起来。
- 基于供给冲击的工具变量策略——包括本文的策略——在资产收益在期限结构上重叠时（如不同期限的国债），通常无法分离出干净识别所需的其他条件不变的价格变化。
- 作者因此将估计的弹性视为简化形式的样本平均参数，而非稳定的结构性参数。
- 部分部门（如家庭部门）的国债持有量是残差估计的，可能包含未正确归类的对冲基金持有量，存在测量误差。

### 与当前研究方向的关联

本文与商业银行、财政政策与货币政策领域的最新学术研究高度相关。它直接研究国债供需变化对收益率的影响，涉及量化宽松、美联储资产负债表政策、公共债务管理、财政与货币政策协调等核心议题。论文使用需求系统方法和工具变量策略，具有明确的识别策略和稳健性检验，政策含义清晰，符合优先选择标准。其关于投资者基础变化影响市场弹性的发现，对理解金融稳定、信用周期和宏观审慎政策具有启示意义。

---

_知识库更新时间：2026-09-19T05:01:12.124622_
