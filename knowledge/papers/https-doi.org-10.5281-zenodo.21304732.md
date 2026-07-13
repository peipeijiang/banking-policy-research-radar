---
title: "多世界贝叶斯个性化排序用于隐式反馈推荐"
paper_id: "https://doi.org/10.5281/zenodo.21304732"
source: "openalex"
published: "2026-07-11T00:00:00"
score: 39.0
tags: ["paper", "recommender-systems", "Recommender Systems and Techniques", "Mobile Crowdsensing and Crowdsourcing", "Explainable Artificial Intelligence (XAI)"]
---

# 多世界贝叶斯个性化排序用于隐式反馈推荐

> **英文原标题**：Multi-World Bayesian Personalized Ranking for Implicit Feedback Recommendation

[查看原文](https://doi.org/10.5281/zenodo.21304732)

## 一句话结论

> 针对隐式反馈推荐中BPR的单空间假设缺陷，提出多世界贝叶斯个性化排序（MWB-BPR），通过并行多兴趣世界建模用户多动机行为，提升排序鲁棒性和用户偏好解耦能力。

## 论文信息

- **作者**：Jincheng Zhang
- **来源**：Zenodo (CERN European Organization for Nuclear Research)
- **发布时间**：2026-07-11
- **相关度评分**：39.0
- **DOI**：[https://doi.org/10.5281/zenodo.21304732](https://doi.org/10.5281/zenodo.21304732)

<details open>
<summary><strong>中文摘要</strong></summary>

推荐系统日益依赖隐式反馈数据（如点击和购买）来捕捉用户偏好。贝叶斯个性化排序（Bayesian Personalized Ranking, BPR）通过优化成对偏好排序，已成为一个基础性框架。然而，经典BPR在严格的“单一确定性假设”下运行，将用户的全部行为历史投射到统一偏好空间中的单一向量上。这种静态表述无法捕捉真实场景中人类行为的多动机性、噪声性和不确定性，导致偏好漂移并对偶然交互缺乏鲁棒性。为放宽这一限制，本文提出一种创新的推荐算法，称为多世界贝叶斯个性化排序（Multi-World Bayesian Personalized Ranking, MWB-BPR）。受模态逻辑中“可能世界”理论的启发，MWB-BPR摒弃了单一空间范式，假设用户同时共存于多个并行的、局部纯净的“兴趣可能世界”中，每个世界代表一种不同的行为动机。在每个世界内部，成对偏好被独立建模，使得矛盾信号能够共存而不相互污染。我们设计了一种基于自注意力的动态世界分配机制，以自适应地计算用户在这些世界中的归属权重。最终，通过全概率公式聚合所有可能世界的预测，得到总体偏好排序。我们为MWB-BPR形式化了完整的贝叶斯最大后验（Maximum a Posteriori, MAP）目标函数，并推导出其梯度更新公式，该公式自然地引入了一个动态的“责任信用”因子，用于在各世界之间分配梯度更新。理论分析表明，MWB-BPR对隐式噪声具有更强的鲁棒性，并擅长解耦复杂的用户动机，为基于排序的个性化推荐提供了一种有前景的新范式。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Recommender systems increasingly rely on implicit feedback data, such as clicks and purchases, to capture user preferences. Bayesian Personalized Ranking (BPR) has emerged as a cornerstone framework by optimizing pairwise preference rankings. However, classic BPR operates under a rigid "unary deterministic assumption," which projects a user's entire behavioral history onto a single vector within a uniform preference space. This static formulation fails to capture the multi-motivational, noisy, and uncertain nature of human behavior in real-world scenarios, leading to preference drift and vulnerability to accidental interactions. To relax this limitation, this paper proposes an innovative recommendation algorithm termed Multi-World Bayesian Personalized Ranking (MWB-BPR). Drawing inspiration from the "possible worlds" theory in modal logic, MWB-BPR discards the single-space paradigm and assumes that a user simultaneously coexists in multiple parallel, locally pure "interest possible worlds," each representing a distinct behavioral motivation. Within each world, pairwise preferences are independently modeled to allow contradictory signals to coexist without cross-contamination. We design a dynamic world assignment mechanism based on self-attention to adaptively calculate the user's belongingness weights across these worlds. Finally, the total preference ranking is derived by aggregating the predictions of all possible worlds using the law of total probability. We formalize the complete Bayesian maximum a posteriori (MAP) objective function for MWB-BPR and derive its gradient update formulations, which naturally introduce a dynamic "responsibility credit" factor to distribute gradient updates among worlds. The theoretical analysis demonstrates that MWB-BPR achieves superior robustness against implicit noise and excels at disentangling complex user motivations, providing a promising new paradigm for ranking-based personalized recommendation.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

本文针对经典贝叶斯个性化排序（BPR）在隐式反馈推荐中的“单变量确定性假设”局限，提出多世界贝叶斯个性化排序（MWB-BPR）算法。受模态逻辑“可能世界”理论启发，MWB-BPR假设用户同时存在于多个平行的“兴趣可能世界”，每个世界代表一种独立的行为动机，并在各世界内独立建模成对偏好，允许矛盾信号共存。通过基于自注意力的动态世界分配机制计算用户在各世界的归属权重，并利用全概率公式融合各世界预测得到最终排序。论文形式化了MWB-BPR的贝叶斯最大后验目标函数，推导了梯度更新公式，其中引入的“责任信用”因子可动态分配梯度更新。理论分析表明，MWB-BPR对隐式噪声具有鲁棒性，并能有效解耦复杂用户动机。

### 主要创新

- 提出多世界假设，将用户兴趣建模为多个平行“可能世界”的叠加，突破单向量表示局限。
- 设计基于自注意力的动态世界权重分配机制，自适应计算用户在各世界的归属概率。
- 利用全概率公式融合各世界偏好预测，使矛盾信号可共存而不相互污染。
- 推导出带“责任信用”因子的梯度更新公式，实现世界间参数更新的自动分工。

### 研究方法

论文采用贝叶斯最大后验（MAP）框架，构建多世界结构下的似然函数和正则化项。通过随机梯度下降（SGD）优化，每步迭代中先计算动态世界权重（基于用户属性向量与世界主题向量的点积经Softmax归一化），再计算各世界局部偏好得分及全局融合概率，最后根据梯度公式更新用户/物品在各世界的嵌入向量及世界权重参数。

### 关键结果

输入内容未提供具体实验数字、数据集或基线对比结果。论文主要从理论上论证了MWB-BPR在噪声鲁棒性、多动机解耦和潜在正样本处理方面的优势。

### 技术栈

- 贝叶斯个性化排序（BPR）
- 最大后验估计（MAP）
- 随机梯度下降（SGD）
- Sigmoid函数
- Softmax函数
- 自注意力机制
- 全概率公式
- L2正则化

### 方法优势

- 理论创新性强，将模态逻辑“可能世界”思想引入推荐系统，开辟新范式。
- 数学推导严谨，完整给出多世界下的MAP目标函数和梯度公式。
- 针对经典BPR的多个固有缺陷（多动机冲突、噪声敏感、潜在正样本惩罚）提出系统性解决方案。
- 动态世界权重机制使模型具有自适应能力。

### 主要局限

- 未提供实验验证，缺乏在真实数据集上的性能对比和消融研究。
- 世界数量K需预设，缺乏自适应调整机制。
- 模型复杂度随世界数K线性增长，可能影响训练效率。
- 动态权重计算依赖用户属性向量，若属性信息不足可能影响效果。

### 与当前研究方向的关联

论文紧密围绕推荐系统隐式反馈和排序问题，提出新方法MWB-BPR，属于用户建模和排序优化方向，与关键词“隐式反馈”、“贝叶斯个性化排序”、“多意图解耦”高度相关。

---

_知识库更新时间：2026-07-12T10:37:28.673902_
