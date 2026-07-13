---
title: "贝叶斯记忆网络BPR：利用外部记忆库进行长期偏好检索"
paper_id: "https://doi.org/10.5281/zenodo.21304776"
source: "openalex"
published: "2026-07-11T00:00:00"
score: 43.0
tags: ["paper", "recommender-systems", "Recommender Systems and Techniques", "Information Retrieval and Search Behavior", "Advanced Bandit Algorithms Research"]
---

# 贝叶斯记忆网络BPR：利用外部记忆库进行长期偏好检索

> **英文原标题**：Bayesian Memory Network BPR: Leveraging External Memory Bank for Long-Term Preference Retrieval

[查看原文](https://doi.org/10.5281/zenodo.21304776)

## 一句话结论

> 针对BPR框架无法保留用户长期偏好的问题，提出BMN-BPR算法，通过集成外部记忆库和贝叶斯动态读取操作，有效捕捉用户长期、多面兴趣，并设计了静态解耦多通道检索策略以实现工业级部署。

## 论文信息

- **作者**：Jincheng Zhang
- **来源**：Zenodo (CERN European Organization for Nuclear Research)
- **发布时间**：2026-07-11
- **相关度评分**：43.0
- **DOI**：[https://doi.org/10.5281/zenodo.21304776](https://doi.org/10.5281/zenodo.21304776)

<details open>
<summary><strong>中文摘要</strong></summary>

在大数据时代，捕捉用户精准且动态变化的偏好仍是个性化推荐系统面临的根本性挑战。尽管经典的贝叶斯个性化排序（Bayesian Personalized Ranking, BPR）框架通过最大化成对排序概率在隐式反馈推荐中取得了显著成功，但其本质上难以在长交互历史中保留用户的长期偏好。传统的基于参数的用户嵌入极易遭受灾难性遗忘，因为由短期、零散交互驱动的连续梯度更新往往会覆盖或扭曲用户潜在、稳定的核心兴趣。为解决这一局限，本文提出一种名为贝叶斯记忆网络BPR（Bayesian Memory Network BPR, BMN-BPR）的新型推荐算法，用于长期偏好检索。BMN-BPR的核心创新在于集成一个显式的、非参数化的外部记忆库，该记忆库系统性地存储并维护用户的多模态后验偏好嵌入。在严格的概率图视角下，我们基于高斯核相似函数开发了一种贝叶斯动态读取算子。该算子使候选项目能够作为线索，灵活激活并唤醒特定的历史兴趣槽位，从而有效捕捉用户兴趣的不确定性与多面性。此外，模型将误差反向传播流作为自然的记忆写入算子，无需经验启发式规则即可动态更新记忆槽位。针对实际部署，我们在召回阶段设计了一种静态解耦的多通道检索策略，将非线性耦合转化为并行近似最近邻搜索（Approximate Nearest Neighbor Search, ANNS）。这一工程化改造同时保证了高推荐多样性与毫秒级在线响应。BMN-BPR为长期用户行为建模提供了坚实的贝叶斯非参数化视角，并为工业级检索系统提供了一种优雅且高度可扩展的解决方案。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

In the era of big data, capturing users' precise and evolving preferences remains a fundamental challenge for personalized recommender systems. Although the classic Bayesian Personalized Ranking (BPR) framework has achieved substantial success in implicit feedback recommendation by maximizing pairwise ranking probabilities, it inherently struggles to retain users' long-term preferences over extended interaction histories. Traditional parameter-based user embeddings are highly susceptible to catastrophic forgetting, as continuous gradient updates driven by short-term, sporadic interactions often overwrite or distort users' underlying, stable core tastes. To address this limitation, this paper proposes a novel recommendation algorithm named Bayesian Memory Network BPR (BMN-BPR) for long-term preference retrieval. The core innovation of BMN-BPR lies in the integration of an explicit, non-parametric external memory bank that systematically stores and maintains users' multi-modal posterior preference embeddings. Within a rigorous probabilistic graphical perspective, we develop a Bayesian dynamic read operator based on a Gaussian kernel similarity function. This operator enables candidate items to act as cues that flexibly activate and awaken specific historical interest slots, effectively capturing the uncertainty and multi-faceted nature of user interests. Furthermore, the model leverages the error backpropagation stream as a natural memory write operator to update the memory slots dynamically without empirical heuristic rules. For real-world deployment, we design a static decoupling multi-channel retrieval strategy for the recall stage, which converts the non-linear coupling into parallel approximate nearest neighbor searches (ANNS). This engineering adaptation guarantees both high recommendation diversity and millisecond-level online response. BMN-BPR provides a solid Bayesian non-parametric perspective for long-term user behavior modeling and offers an elegant, highly scalable solution for industry-scale retrieval systems.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

本文针对传统BPR算法在长期交互场景下难以保留用户长期偏好的问题，提出贝叶斯记忆网络BPR（BMN-BPR）。该模型引入外部非参数记忆库存储用户多模态后验偏好嵌入，通过基于高斯核相似性的贝叶斯动态读取算子，使候选项目作为线索激活特定历史兴趣槽，并利用误差反向传播作为自然写入算子更新记忆槽。在召回阶段，设计静态解耦多通道检索策略，将非线性耦合转换为并行近似最近邻搜索，保证多样性和毫秒级响应。BMN-BPR为长期用户行为建模提供了贝叶斯非参数视角，并为工业级检索系统提供了可扩展方案。

### 主要创新

- 提出将外部非参数记忆库与BPR框架结合，用于长期偏好检索。
- 设计基于高斯核相似性的贝叶斯动态读取算子，实现候选项目对历史兴趣槽的灵活激活。
- 利用误差反向传播作为记忆写入算子，无需启发式规则。
- 提出静态解耦多通道检索策略，将非线性读取转换为并行ANNS，兼顾多样性和效率。

### 研究方法

BMN-BPR模型包括项目嵌入层、外部后验记忆库、贝叶斯读取算子和成对排序层。每个用户分配K个记忆槽，读取时计算项目嵌入与各槽的高斯核相似性作为注意力权重，加权求和得到用户实时偏好嵌入。训练采用BPR成对排序损失，梯度反向传播更新记忆槽和项目嵌入。召回阶段将K个记忆槽作为独立查询向量进行ANNS，合并结果。

### 关键结果

输入内容未提供

### 技术栈

- 贝叶斯个性化排序（BPR）
- 外部记忆网络（Memory Network）
- 高斯核相似性函数
- 随机梯度下降（SGD）
- 近似最近邻搜索（ANNS）
- Frobenius范数正则化

### 方法优势

- 理论严谨：从贝叶斯概率图模型角度解释记忆读写操作。
- 解决长期偏好遗忘问题：通过外部记忆槽隔离长期与短期兴趣。
- 工程实用：静态解耦策略使召回阶段高效且可扩展。
- 方法创新：将非参数记忆与成对排序优化有机融合。

### 主要局限

- 未提供实验验证和定量结果，缺乏与基线方法的比较。
- 记忆槽数量K为超参数，需人工设定，可能影响性能。
- 模型复杂度较高，每个用户需独立维护K个记忆向量，存储开销大。
- 静态解耦近似可能损失读取算子的非线性表达能力。

### 与当前研究方向的关联

序列推荐：相关，模型关注长期偏好序列建模。；用户建模：高度相关，通过记忆槽建模用户多模态偏好。；推荐系统工业落地：相关，设计了高效召回策略。；排序与重排：相关，基于BPR成对排序框架。

---

_知识库更新时间：2026-07-12T10:37:28.673708_
