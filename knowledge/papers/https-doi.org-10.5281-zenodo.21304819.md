---
title: "Research on Personalized Ranking Recommendation Algorithm Based on Local Bayesian Neighborhood"
paper_id: "https://doi.org/10.5281/zenodo.21304819"
source: "openalex"
published: "2026-07-11T00:00:00"
score: 36.0
tags: ["paper", "recommender-systems", "Recommender Systems and Techniques", "Advanced Technologies in Various Fields", "Advanced Data and IoT Technologies"]
---

# Research on Personalized Ranking Recommendation Algorithm Based on Local Bayesian Neighborhood

[查看原文](https://doi.org/10.5281/zenodo.21304819)

## 一句话结论

> 针对BPR算法忽略用户兴趣局部集中性的问题，提出LBN-BPR算法，通过局部贝叶斯邻域优化，提升隐式反馈场景下的个性化排序性能。

## 论文信息

- **作者**：Jincheng Zhang
- **来源**：Zenodo (CERN European Organization for Nuclear Research)
- **发布时间**：2026-07-11
- **相关度评分**：36.0
- **DOI**：[https://doi.org/10.5281/zenodo.21304819](https://doi.org/10.5281/zenodo.21304819)

<details open>
<summary><strong>中文摘要</strong></summary>

在信息爆炸时代，推荐系统已成为缓解信息过载问题的核心技术。隐式反馈（如点击、浏览和购买）因其易于收集的特性，已成为训练推荐模型的主要数据来源。贝叶斯个性化排序（Bayesian Personalized Ranking, BPR）作为一种经典的成对偏好排序算法，在处理隐式反馈方面展现出卓越性能。然而，传统BPR在参数优化过程中采用全局采样与全局更新策略，容易忽视用户兴趣的局部集中性，导致模型极易受到全局稀疏噪声的干扰，从而难以捕捉细粒度的局部用户偏好。针对上述局限，本文提出一种名为局部贝叶斯邻域BPR（Local Bayesian Neighborhood BPR, LBN-BPR）的新型推荐算法。该算法的核心思想是严格在用户局部高相似邻域内定义并优化后验概率，从而使训练过程免受全局噪声干扰。LBN-BPR首先利用先进的语义相似度度量方法为每位用户构建局部邻域空间，并在此基础上建立局部贝叶斯优化框架。通过约束随机梯度下降（Stochastic Gradient Descent, SGD）的更新范围，模型参数得以聚焦于与目标用户具有相似行为特征的局部子群体进行训练。理论分析与梯度推导表明，LBN-BPR能够以更高精度拟合局部个性化偏好。本文详细阐述了LBN-BPR的理论基础、建模过程、优化策略及复杂度分析，为隐式反馈场景下的高质量个性化推荐提供了一种鲁棒且抗噪声的解决方案。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

In the era of information explosion, recommender systems have emerged as a core technology to alleviate the problem of information overload. Implicit feedback (e.g., clicks, views, and purchases) has become the primary data source for training recommendation models due to its ease of collection. Bayesian Personalized Ranking (BPR), a classic pairwise preference ranking algorithm, has demonstrated outstanding performance in handling implicit feedback. However, traditional BPR employs global sampling and global update strategies during parameter optimization, which tends to overlook the local concentration of user interests. Consequently, the model is highly susceptible to global sparsity noise, leading to an insufficient capacity for capturing fine-grained, localized user preferences. To address these limitations, this paper proposes a novel recommendation algorithm named Local Bayesian Neighborhood BPR (LBN-BPR). The core philosophy of this algorithm is to define and optimize the posterior probability strictly within a user's localized, highly-similar neighborhood, thereby insulating the training process from global noise interference. LBN-BPR first constructs a local neighborhood space for each user using an advanced semantic similarity metric, and then establishes a local Bayesian optimization framework on top of it. By constraining the update range of Stochastic Gradient Descent (SGD), the model parameters are trained to focus heavily on the local sub-communities that share similar behavioral characteristics with the target user. Theoretical analysis and gradient derivations demonstrate that LBN-BPR can fit localized personalized preferences with higher precision. This paper thoroughly elaborates on the theoretical foundations, modeling processes, optimization strategies, and complexity analyses of LBN-BPR, providing a robust and noise-resistant solution for high-quality personalized recommendation under implicit feedback scenarios.

</details>

---

_知识库更新时间：2026-07-13T01:23:50.735430_
