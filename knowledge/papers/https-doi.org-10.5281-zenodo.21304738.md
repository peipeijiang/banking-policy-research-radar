---
title: "Causal-BPR：面向曝光偏差的无偏推荐因果贝叶斯个性化排序"
paper_id: "https://doi.org/10.5281/zenodo.21304738"
source: "openalex"
published: "2026-07-11T00:00:00"
score: 51.0
tags: ["paper", "recommender-systems", "Recommender Systems and Techniques", "Advanced Bandit Algorithms Research", "Explainable Artificial Intelligence (XAI)"]
---

# Causal-BPR：面向曝光偏差的无偏推荐因果贝叶斯个性化排序

> **英文原标题**：Causal-BPR: Causal Bayesian Personalized Ranking for Unbiased Recommendation under Exposure Bias

[查看原文](https://doi.org/10.5281/zenodo.21304738)

## 一句话结论

> 提出Causal-BPR框架，通过结构因果模型解耦用户交互中的因果兴趣路径和曝光偏差路径，结合逆倾向评分和因果感知负采样，实现无偏的贝叶斯个性化排序，缓解曝光偏差导致的马太效应。

## 论文信息

- **作者**：Jincheng Zhang
- **来源**：Zenodo (CERN European Organization for Nuclear Research)
- **发布时间**：2026-07-11
- **相关度评分**：51.0
- **DOI**：[https://doi.org/10.5281/zenodo.21304738](https://doi.org/10.5281/zenodo.21304738)

<details open>
<summary><strong>中文摘要</strong></summary>

依赖隐式反馈的推荐系统常遭受严重的曝光偏差，因为未观测到的交互中混杂着真实负反馈以及因系统排序策略而未被曝光的物品。标准成对推荐算法（如贝叶斯个性化排序，BPR）基于观测到的相关性而非真实用户偏好进行优化，导致“富者愈富”的马太效应及次优的排序性能。为解决这些挑战，本文提出Causal-BPR——一种新颖的因果贝叶斯个性化排序框架，利用结构因果模型（SCM）将用户交互解耦为不同路径。具体而言，我们区分“因果兴趣路径”与“曝光偏差路径”，以将真实用户偏好与系统性可见性相分离。基于此因果图分解，我们引入反事实优化机制，该机制仅沿因果路径执行贝叶斯后验更新。通过将逆倾向评分（IPS）融入成对损失并设计因果感知负采样策略，Causal-BPR在理论上将有偏的观测经验风险转化为无偏的理想风险估计。理论分析证明，我们的框架实现了渐近因果无偏性，并在裁剪约束下保持有界梯度方差。本工作完成了从因果分解到稳健参数估计的严格理论闭环，为缓解隐式反馈Top-N推荐中的曝光偏差提供了坚实的数学基础。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Recommender systems relying on implicit feedback often suffer from severe exposure bias, as unobserved interactions are mixed with true negative feedback and items left unexposed due to system ranking policies. Standard pairwise recommendation algorithms, such as Bayesian Personalized Ranking (BPR), optimize based on observed correlations rather than true user preferences, leading to the "rich-get-richer" Matthew effect and suboptimal ranking performance. To address these challenges, this paper proposes Causal-BPR, a novel causal Bayesian personalized ranking framework that decouples user interactions into distinct pathways using structural causal models (SCMs). Specifically, we distinguish the "causal interest pathway" from the "exposure bias pathway" to isolate true user preferences from systemic visibility. Based on this causal graph decomposition, we introduce a counterfactual optimization mechanism that executes Bayesian posterior updates exclusively along the causal pathway. By incorporating inverse propensity scoring (IPS) into the pairwise loss and designing a causal-aware negative sampling strategy, Causal-BPR theoretically transforms the biased observational empirical risk into an unbiased ideal risk estimation. Theoretical analysis proves that our framework achieves asymptotic causal unbiasedness and maintains bounded gradient variance under clipping constraints. This work completes a rigorous theoretical loop from causal factorization to robust parameter estimation, providing a solid mathematical foundation for mitigating exposure bias in implicit-feedback top-N recommendation.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

针对隐式反馈推荐系统中因曝光偏差导致未交互项混杂真实负反馈与未曝光项的问题，本文提出Causal-BPR框架。通过结构因果模型将用户交互解耦为因果兴趣路径和曝光偏差路径，仅沿因果路径进行贝叶斯后验更新。引入逆倾向评分加权成对损失和因果感知负采样策略，理论上将有偏观测经验风险转化为无偏理想风险估计。理论分析证明框架渐近因果无偏性，并在截断约束下保持有界梯度方差。

### 主要创新

- 提出基于结构因果模型的点击行为因果解耦方法，区分因果兴趣路径与曝光偏差路径。
- 设计仅沿因果路径进行贝叶斯后验更新的优化框架，实现无偏参数估计。
- 引入逆倾向评分加权成对损失函数，将观测经验风险转化为无偏理想风险。
- 提出因果感知负采样策略，优先采样高曝光但未点击的负样本以增强因果信息。
- 理论证明算法渐近因果无偏性，并分析截断超参数对偏差-方差权衡的影响。

### 研究方法

采用结构因果模型对用户点击行为进行因果图分解，定义因果兴趣路径和曝光偏差路径。基于潜在结果框架定义真实因果效应C_ui，并通过后门准则推导可估计的因果解耦方程。在矩阵分解架构下设置独立的因果兴趣空间和曝光偏差空间，分别建模C_ui和O_ui。利用逆倾向评分加权成对损失函数，结合因果感知负采样策略，通过随机梯度下降优化因果参数。

### 关键结果

输入内容未提供

### 技术栈

- 结构因果模型
- 贝叶斯个性化排序
- 矩阵分解
- 逆倾向评分
- 随机梯度下降
- 后门准则
- 潜在结果框架
- sigmoid函数
- 最大后验概率估计

### 方法优势

- 从因果角度系统分析了曝光偏差对BPR的影响，理论框架完整。
- 提出明确的因果解耦方程和可计算的因果效应定义。
- 通过逆倾向评分加权实现理论上的无偏估计，并给出渐近无偏性证明。
- 设计了因果感知负采样策略，提升训练效率。
- 对梯度方差和收敛性进行了理论分析，考虑了偏差-方差权衡。

### 主要局限

- 未进行实验验证，缺乏实际数据集上的性能评估。
- 倾向评分估计依赖全局统计或双塔模型，未讨论估计误差的影响。
- 假设未曝光项点击概率为零，可能忽略用户主动忽略的情况。
- 未讨论多任务学习或联合训练中曝光参数与因果参数的交互。
- 未提供与现有去偏方法的对比分析。

### 与当前研究方向的关联

推荐系统：核心研究领域，提出推荐算法Causal-BPR。；因果性：核心创新点，利用因果推断解决曝光偏差。；排序与重排：针对Top-N排序任务，优化贝叶斯个性化排序。；用户建模：通过因果解耦建模用户真实兴趣。；CTR/CVR预测：涉及点击行为建模，但未直接预测点击率。

---

_知识库更新时间：2026-07-12T10:37:28.673020_
