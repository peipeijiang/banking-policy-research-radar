---
title: "向量自回归中的阈值内生性：重新评估货币状态依赖性"
paper_id: "ecb:https://www.ecb.europa.eu//pub/pdf/scpwps/ecb.wp3263~54951460ab.en.pdf"
source: "ecb"
published: "2026-07-29T09:00:00"
score: 80.0
tags: ["paper", "banking-fiscal-monetary-policy"]
---

# 向量自回归中的阈值内生性：重新评估货币状态依赖性

> **英文原标题**：Threshold endogeneity in vector autoregressions: reassessing monetary state dependence

[查看原文](https://www.ecb.europa.eu//pub/pdf/scpwps/ecb.wp3263~54951460ab.en.pdf)

## 一句话结论

> 提出内生阈值VAR方法解决阈值变量与冲击的同期依赖问题，应用于货币政策传导，避免线性VAR的谜题，估计体制依赖的牺牲比率。

## 论文信息

- **作者**：-
- **来源**：ECB Working Papers
- **发布时间**：2026-07-29
- **相关度评分**：80.0
- **DOI**：-

## 相关性评分

- **商业银行**：0.0/10
- **货币政策**：8.0/10（最高匹配）
- **财政政策**：0.0/10

<details open>
<summary><strong>中文摘要</strong></summary>

我们构建了一个内生阈值向量自回归模型，用以解决阈值变量与简化式新息之间的同期依赖关系——当机制指标与系统动态共同决定时，这一普遍存在的问题便会出现。一种基于机制特定连接函数的控制函数，无需工具变量，也无需对阈值的边际分布进行参数假设，即可消除这种依赖，同时保留线性机制层面的最小二乘结构。我们通过脉冲响应中的过度敏感性和过度传播误差来刻画由此产生的设定偏误，阐明内生机制下的结构识别与代理变量SVAR识别，并建立陈氏类型阈值渐近性在使用生成控制变量时仍然有效的条件。赫尔米特样条扩展方法可处理尾部依赖与非对称依赖。蒙特卡洛证据表明，忽略内生性会导致严重的扭曲。将该框架应用于货币传导机制时，它避免了线性VAR所呈现的价格谜题与持续性谜题，提供了机制依赖的牺牲率，并将估计出的机制与历史上的通胀阶段相对应。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

We develop an endogenous threshold VAR that addresses contemporaneous dependence between the threshold variable and reduced-form innovations— a pervasive issue when regime indicators are jointly determined with system dynamics. A regime-specific copula-based control function removes this dependence instrument-free, without parametric assumptions on the threshold’s marginal distribution, while preserving the linear regime-wise least-squares structure. We characterize the resulting misspecification through excess sensitivity and excess propagation errors in impulse responses, clarify structural and proxy-SVAR identification under endogenous regimes, and establish conditions under which Chan-type threshold asymptotics remain valid with generated controls. A Hermite sieve extension accommodates tail-dependent and asymmetric dependence. Monte Carlo evidence documents large distortions from ignoring endogeneity. Applied to monetary transmission, the framework avoids the price and persistence puzzles displayed by the linear VAR, delivers regime-dependent sacrifice ratios, and aligns estimated regimes with historical inflation episodes.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

本文提出一种内生阈值向量自回归（TVAR）模型，解决阈值变量与简化式创新之间的同期相关性——当状态指标与系统动态联合决定时，这一问题普遍存在。通过基于copula的机制特定控制函数，在不依赖外部工具或阈值边际分布参数假设的前提下，消除这种相关性，同时保留线性机制内最小二乘结构。研究表明，忽略控制函数会导致脉冲响应中的“过度敏感性”和“过度传播”误差，并阐明内生机制下的结构识别和代理SVAR识别条件。蒙特卡洛实验验证了忽略内生性在不同设计下的偏差大小。应用于货币政策传导分析时，该框架避免了线性VAR的价格谜题和持久性谜题，提供了机制依赖的牺牲比率，并将估计的机制与历史通胀阶段对齐。

### 主要创新

- 首次在多变量VAR环境中解决阈值内生性问题，提出基于copula的控制函数方法。
- 推导了忽略阈值内生性导致的脉冲响应误差分解：过度敏感性（影响矩阵膨胀）和过度传播（动态系数偏误）。
- 建立了内生机制下结构识别和代理SVAR识别的条件，并证明了Chan型阈值渐近性在生成控制变量下仍然有效。
- 提出Hermite筛扩展以处理尾部依赖和非对称依赖结构。

### 研究方法

论文采用理论推导与蒙特卡洛模拟相结合的方法。首先，基于高斯copula假设推导出阈值变量与创新向量之间的单因子控制函数表示，并将其嵌入TVAR模型。然后，通过理论分析刻画忽略内生性导致的方差膨胀、系数偏误和脉冲响应误差。最后，通过蒙特卡洛实验验证方法的有效性，并应用于美国货币政策传导的实证分析。

### 关键结果

忽略阈值内生性会导致简化式创新方差膨胀（Σ_uu = ΛΛ' + Σ_εε），且系数估计产生遗漏变量偏误（ΔA = Λγ）。；脉冲响应误差可分解为过度敏感性（影响矩阵膨胀）和过度传播（动态乘子偏误），两者均与加载向量Λ一阶相关。；蒙特卡洛实验表明，未校正的TVAR在阈值估计、机制特定协方差矩阵和脉冲响应上存在显著偏差，而校正后的TVAR大幅降低偏差和均方误差。；实证应用中，内生阈值VAR估计的阈值约为3.34%，机制分类与历史通胀阶段一致，且脉冲响应避免了价格谜题，高通胀机制下牺牲比率更高。

### 技术栈

- 高斯copula
- 概率积分变换（PIT）
- 控制函数方法
- 最小二乘估计
- Chan型阈值渐近理论
- Hermite筛扩展
- 蒙特卡洛模拟
- 脉冲响应分析
- 结构VAR识别（递归、符号约束、外部工具）

### 方法优势

- 首次系统解决TVAR中的阈值内生性问题，理论贡献明确。
- 方法具有实用性：无需外部工具或阈值分布参数假设，保留线性机制内结构。
- 提供了完整的理论推导和误差分解，清晰揭示忽略内生性的后果。
- 蒙特卡洛实验设计全面，涵盖多种依赖结构、分布和样本量。
- 实证应用具有政策相关性，结果与经济学直觉一致。

### 主要局限

- 基准模型假设高斯copula，虽然通过Hermite筛扩展，但非高斯依赖结构下的有限样本表现需进一步验证。
- 方法依赖于阈值变量连续且严格递增的CDF假设，离散或跳跃性阈值可能不适用。
- 实证部分仅使用美国数据，结论的普适性需在其他经济体或不同阈值变量下检验。
- 未讨论阈值变量本身动态过程的建模，仅将其视为外生给定。

### 与当前研究方向的关联

论文直接研究货币政策传导中的状态依赖性，与“货币政策”、“利率与通胀”、“中央银行政策工具”高度相关。其内生阈值方法可应用于金融稳定和信用周期分析，与“金融稳定”、“信用周期”相关。同时，论文涉及结构识别和脉冲响应，与“宏观审慎政策”和“财政与货币政策协调”的方法论相关。

---

_知识库更新时间：2026-07-30T03:49:12.776063_
