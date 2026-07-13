---
title: "面向高效对话式推荐：信息期望价值与Bandit学习的融合"
paper_id: "https://doi.org/10.1145/3696410.3714773"
source: "www"
published: "2025-01-01T00:00:00"
score: 38.0
tags: ["paper", "recommender-systems", "Advanced Bandit Algorithms Research", "Data Stream Mining Techniques", "Recommender Systems and Techniques"]
---

# 面向高效对话式推荐：信息期望价值与Bandit学习的融合

> **英文原标题**：Towards Efficient Conversational Recommendations: Expected Value of Information Meets Bandit Learning

[查看原文](https://dblp.org/rec/conf/www/0001LDL25) · [Semantic Scholar](https://www.semanticscholar.org/paper/7e00fa6b8a7d97fd9ae6e5ece31201f8c6af16a2)

## 一句话结论

> 该论文将期望信息价值（EVOI）集成到对话式推荐框架中，提出梯度EVOI和平滑关键术语上下文两种技术，显著降低了计算复杂度并提供了更紧的遗憾界。

## 论文信息

- **作者**：Zhuohua Li, Maoli Liu, Xiangxiang Dai, John C. S. Lui
- **来源**：WWW
- **发布时间**：2025-01-01
- **相关度评分**：38.0
- **DOI**：[https://doi.org/10.1145/3696410.3714773](https://doi.org/10.1145/3696410.3714773)

<details open>
<summary><strong>中文摘要</strong></summary>

在对话式推荐系统中，交互式呈现查询并利用用户反馈对于高效估计用户偏好及提升推荐质量至关重要。在这些系统中选择最优查询是一项重大挑战，已被广泛研究为序贯决策问题。信息期望值（EVOI）通过计算期望奖励提升，为查询选择提供了理论依据。然而，该方法计算成本高昂且缺乏理论性能保证。相反，对话式强盗算法提供了可证明的遗憾上界，但其查询选择策略相较于非对话式方法仅带来微小的遗憾改进。为解决这些局限，我们将EVOI整合至对话式强盗框架中，提出了一种新的对话机制，该机制包含两项关键技术：（1）基于梯度的EVOI，用高效的随机梯度下降替代传统EVOI中复杂的贝叶斯更新，显著降低计算复杂度并便于理论分析；（2）平滑化关键术语上下文，通过添加随机扰动增强探索，以揭示更具体的用户偏好。我们的方法适用于对话式强盗算法的贝叶斯（汤普森采样）和频率学派（UCB）变体。我们提出了两种新算法ConTS-EVOI和ConUCB-EVOI，并严格证明它们实现了更紧致的遗憾上界，两种算法在时间范围T上的依赖度均获得了√d的改进，其中d为特征空间维度。在合成数据集与真实世界数据集上的广泛评估验证了我们方法的有效性。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

In conversational recommender systems, interactively presenting queries and leveraging user feedback are crucial for efficiently estimating user preferences and improving recommendation quality. Selecting optimal queries in these systems is a significant challenge that has been extensively studied as a sequential decision problem. The expected value of information (EVOI), which computes the expected reward improvement, provides a principled criterion for query selection. However, it is computationally expensive and lacks theoretical performance guarantees. Conversely, conversational bandits offer provable regret upper bounds, but their query selection strategies yield only marginal regret improvements over non-conversational approaches. To address these limitations, we integrate EVOI within the conversational bandit framework by proposing a new conversational mechanism featuring two key techniques: (1) gradient-based EVOI, which replaces the complex Bayesian updates in conventional EVOI with efficient stochastic gradient descent, significantly reducing computational complexity and facilitating theoretical analysis; and (2) smoothed key term contexts, which enhance exploration by adding random perturbations to uncover more specific user preferences. Our approach applies to both Bayesian (Thompson Sampling) and frequentist (UCB) variants of conversational bandits. We introduce two new algorithms, ConTS-EVOI and ConUCB-EVOI, and rigorously prove that they achieve substantially tighter regret bounds, with both algorithms offering a √d improvement in their dependence on the time horizon T, where d is the dimension of the feature space. Extensive evaluations on synthetic and real-world datasets validate the effectiveness of our methods.

</details>

## 深度解读

> 分析依据：**摘要分析**

### 核心结论

对话式推荐系统中，通过交互式查询和用户反馈高效估计用户偏好并提升推荐质量是关键挑战。现有方法中，信息期望价值（EVOI）虽提供理论最优查询选择准则，但计算复杂且缺乏性能保证；对话式Bandit虽具有可证明的遗憾上界，但查询选择策略带来的遗憾改进有限。本文提出融合EVOI与对话式Bandit的新机制，包含两项关键技术：梯度化EVOI，用随机梯度下降替代复杂贝叶斯更新，降低计算复杂度并便于理论分析；平滑化关键术语上下文，通过随机扰动增强探索以发现更具体的用户偏好。该方法适用于贝叶斯（汤普森采样）和频率派（UCB）两种对话式Bandit变体，提出ConTS-EVOI和ConUCB-EVOI算法，并严格证明两者均实现更紧的遗憾界，在时间T上的依赖度改进√d（d为特征空间维度）。合成与真实数据集上的广泛评估验证了方法的有效性。

### 主要创新

- 提出梯度化EVOI，用随机梯度下降替代传统贝叶斯更新，大幅降低计算复杂度并便于理论分析。
- 引入平滑化关键术语上下文，通过随机扰动增强探索，挖掘更具体的用户偏好。
- 将EVOI无缝集成到对话式Bandit框架中，同时适用于汤普森采样和UCB两种变体。
- 理论证明新算法ConTS-EVOI和ConUCB-EVOI实现更紧的遗憾界，在时间T上的依赖度改进√d。

### 研究方法

本文采用理论分析与实验验证相结合的方法。首先，将EVOI与对话式Bandit框架融合，提出梯度化EVOI和平滑化关键术语上下文两项技术。梯度化EVOI利用随机梯度下降近似EVOI，避免复杂贝叶斯更新；平滑化关键术语上下文通过添加随机扰动增强探索。基于此，分别针对贝叶斯（汤普森采样）和频率派（UCB）对话式Bandit设计ConTS-EVOI和ConUCB-EVOI算法。理论部分推导遗憾上界，证明改进的√d因子。实验部分在合成和真实数据集上评估算法性能。

### 关键结果

提出ConTS-EVOI和ConUCB-EVOI两种新算法。；严格证明两种算法均实现更紧的遗憾界，在时间T上的依赖度改进√d（d为特征空间维度）。；合成和真实数据集上的广泛评估验证了方法的有效性。

### 技术栈

- 信息期望价值（EVOI）
- 对话式Bandit框架
- 随机梯度下降（SGD）
- 汤普森采样（Thompson Sampling）
- UCB（Upper Confidence Bound）
- 遗憾界分析

### 方法优势

- 创新性地融合EVOI与对话式Bandit，兼顾理论最优性与可证明遗憾界。
- 梯度化EVOI显著降低计算复杂度，使方法实用。
- 平滑化关键术语上下文增强探索，提升推荐质量。
- 理论证明遗憾界改进√d，具有显著理论贡献。
- 适用于贝叶斯和频率派两种主流Bandit方法，通用性强。

### 主要局限

- 论文局限：摘要未提供具体实验数据集、基线模型、消融实验及参数设置，无法评估实际性能对比。
- 当前证据局限：仅基于摘要分析，缺乏对方法局限性（如对高维特征空间的扩展性、用户反馈噪声敏感性等）的讨论。

### 与当前研究方向的关联

{'对话式推荐': '核心研究主题，论文聚焦对话式推荐系统中的查询选择和用户偏好估计。', 'Bandit学习': '论文将EVOI与对话式Bandit框架结合，提出新算法并给出遗憾界。', '推荐系统': '属于推荐系统领域，特别是交互式推荐。', '用户建模': '通过查询和反馈估计用户偏好，涉及用户建模。', '序列推荐': '对话式推荐可视为序列决策过程，但论文未明确提及序列推荐。'}

---

_知识库更新时间：2026-07-13T01:23:50.735815_
