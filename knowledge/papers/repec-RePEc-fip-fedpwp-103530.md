---
title: "充足准备金动态"
paper_id: "repec:RePEc:fip:fedpwp:103530"
source: "philadelphia_fed"
published: "2026-07-15T00:00:00"
score: 90.0
tags: ["paper", "banking-fiscal-monetary-policy"]
---

# 充足准备金动态

> **英文原标题**：The Dynamics of Ample Reserves

[查看原文](https://ideas.repec.org/p/fip/fedpwp/103530.html)

## 一句话结论

> 研究充足准备金水平与流动性存款的动态关系，发现准备金供给与存款创造存在反馈循环，可能导致不稳定，通过校准模拟分析其影响。

## 论文信息

- **作者**：Roc Armenter
- **来源**：Working Papers
- **发布时间**：2026-07-15
- **相关度评分**：90.0
- **DOI**：10.21799/frbp.wp.2026.34

## 相关性评分

- **商业银行**：2.0/10
- **货币政策**：9.0/10（最高匹配）
- **财政政策**：1.0/10

<details open>
<summary><strong>中文摘要</strong></summary>

货币政策的实施方式会对中央银行的资产负债表动态产生重大影响。如果流动性存款增加了对准备金的需求（Lopez-Salido and Vissing-Jorgensen 2025），那么为缩小政策利率与准备金利率之间的利差所需的“充足”准备金水平本身便是流动性存款的函数。准备金供给在首次达到充足水平后将继续正常化，直至流动性存款也回归趋势。此外，如果准备金供给鼓励了存款创造（Acharya et al. 2024），则会产生一个反馈循环，该循环可能放大存款高企的持续性，甚至引发爆炸性动态。一项现成的校准实验发现，即便只是微小的内在存款持续性也可能触发爆炸性动态。减弱充足准备金对存款的响应，能够以利率偏差方面的适度成本消除不稳定性风险。基于稳定根的模拟显示，准备金首次达到充足水平的时间早于且水平高于仅由准备金需求所预期的结果。然而，此后准备金供给可能进一步下降（至少相对于趋势而言），因为流动性存款在过渡期内仍保持高企。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

How monetary policy is implemented can have significant implications for the dynamics of the central bank’s balance sheet. If liquid deposits increase the demand for reserves (Lopez-Salido and Vissing-Jorgensen 2025), then the “ample” level of reserves needed to close the spread between the policy rate and interest on reserves is itself a function of liquid deposits. The supply of reserves will continue to normalize after first reaching ample levels and until liquid deposits return to trend as well. Furthermore, if the supply of reserves encourages deposit creation (Acharya et al. 2024), then a feedback loop arises that can amplify the persistence of elevated deposits and even lead to explosive dynamics. An off-the-shelf calibration exercise finds that even modest amounts of intrinsic deposit persistence could trigger explosive dynamics. Attenuating the response of ample reserves to deposits removes the risk of instability at a modest cost in terms of rate deviations. Simulations with stable roots show that reserves first reach ample earlier and at a higher level than expected by the demand of reserves alone. However, the supply of reserves may decrease further thereafter, at least relative to trend, as liquid deposits remain elevated in the transition period.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

本文研究货币政策实施如何影响央行资产负债表动态。若流动性存款增加准备金需求（Lopez-Salido和Vissing-Jorgensen 2025），则关闭政策利率与准备金利率之间利差所需的“充足”准备金水平本身是存款的函数。准备金供给在首次达到充足水平后将继续正常化，直至流动性存款也回归趋势。此外，若准备金供给鼓励存款创造（Acharya等人2024），则会产生反馈循环，放大存款持续高企的持久性，甚至导致爆炸性动态。校准发现，即使适度的内在存款持久性也可能触发不稳定性。削弱充足准备金对存款的响应可消除不稳定风险，但代价是利差小幅波动。模拟显示，准备金首次达到充足的时间早于且水平高于仅考虑准备金需求时的预期，但此后准备金供给可能进一步下降（至少相对趋势而言），因为流动性存款在过渡期仍保持高位。

### 主要创新

- 将准备金需求与存款创造两个独立文献的方程耦合，构建反馈循环模型。
- 提出充足准备金水平随流动性存款动态变化的观点，挑战静态充足水平假设。
- 识别反馈循环导致爆炸性动态的条件，并给出稳定性条件。
- 提出“衰减”策略（削弱充足准备金对存款的响应）作为消除不稳定风险的工具。
- 通过校准和模拟展示QE-QT-RMP过程中准备金和存款的动态路径。

### 研究方法

构建一个由两个方程组成的局部线性确定性模型：准备金需求方程（来自Lopez-Salido和Vissing-Jorgensen 2025）和存款创造方程（来自Acharya等人2024）。模型以对数偏离趋势的形式表示，通过逆推准备金需求得到充足准备金方程，并耦合存款创造方程得到一维存款动态系统。稳定性条件通过特征根分析得出。使用点估计进行校准，并模拟QE-QT-RMP情景下的动态。

### 关键结果

充足准备金对存款的弹性约为1.4，反馈强度约为0.3。；稳定性条件为γ_m * (-φ_d/φ_m) + ρ_d < 1，其中ρ_d为存款内在持久性。；在点估计下，ρ_d > 0.7（季度频率）时系统不稳定。；模拟显示，准备金首次达到充足时存款仍高于趋势，因此充足准备金水平高于趋势水平，且此后准备金供给继续相对趋势下降。；衰减（α=1）可降低系统持久性，但引入暂时性正利差。

### 技术栈

- 对数线性化
- 一阶差分方程
- 特征根稳定性分析
- 校准
- 确定性模拟

### 方法优势

- 模型简洁，仅用两个方程捕捉核心反馈机制。
- 基于已有实证文献的参数估计，具有现实基础。
- 明确给出稳定性条件，便于政策讨论。
- 提出衰减策略，具有政策可操作性。
- 模拟结果直观展示动态路径，有助于理解过渡过程。

### 主要局限

- 模型为局部线性近似，缺乏全局性质。
- 未考虑其他可能影响准备金需求的因素（如支付系统）。
- 存款创造方程存在“缺失截距”问题，校准依赖点估计。
- 未包含ON RRP利率等非线性因素。
- 缺乏对充足准备金方程的直接实证验证。

### 与当前研究方向的关联

本文直接涉及中央银行政策工具（准备金供给、利率控制）、量化宽松（QE/QT）、金融稳定（反馈循环导致的不稳定性）、银行信贷与风险承担（存款创造渠道）、货币政策实施（充足准备金制度）。与关键词高度相关。

<details>
<summary><strong>发现与关联证据</strong></summary>

- **provider**：IDEAS/RePEc
- **series_url**：https://ideas.repec.org/s/fip/fedpwp.html
- **free_download**：True
- **date_precision**：day

</details>

---

_知识库更新时间：2026-07-17T03:55:06.419176_
