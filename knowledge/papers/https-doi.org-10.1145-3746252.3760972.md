---
title: "Dual Context-Aware Negative Sampling Strategy for Graph-based Collaborative Filtering"
paper_id: "https://doi.org/10.1145/3746252.3760972"
source: "cikm"
published: "2025-01-01T00:00:00"
score: 28.0
tags: ["paper", "recommender-systems", "Recommender Systems and Techniques", "Mobile Crowdsensing and Crowdsourcing", "Domain Adaptation and Few-Shot Learning"]
---

# Dual Context-Aware Negative Sampling Strategy for Graph-based Collaborative Filtering

[查看原文](https://dblp.org/rec/conf/cikm/0009ZYFPG25) · [Semantic Scholar](https://www.semanticscholar.org/paper/b0e4c6a5bb30cd7f4c6be5f969744734fdf16cb0)

## 一句话结论

> 论文提出双上下文感知负采样策略（DCANS），通过评估正样本与用户兴趣的对齐程度并调整合成负样本的难度，缓解隐式反馈中的假阳性问题，提升推荐性能。

## 论文信息

- **作者**：Xi Wu, Wenzhe Zhang, Liangwei Yang, Xiaohan Fang, Jiquan Peng, Jibing Gong
- **来源**：CIKM
- **发布时间**：2025-01-01
- **相关度评分**：28.0
- **DOI**：[https://doi.org/10.1145/3746252.3760972](https://doi.org/10.1145/3746252.3760972)

<details open>
<summary><strong>中文摘要</strong></summary>

负采样在协同过滤（collaborative filtering, CF）中扮演着关键角色，因为它能加速收敛并提升推荐精度。在近期研究中，基于混合（mixup）的负采样方法展现了良好的性能。然而，现有方法主要关注增加合成负样本与正样本之间的相似度，而未考虑隐式反馈场景中常见的假阳性问题。盲目地使用过难负样本训练所有正样本，会放大假阳性的影响并损害推荐性能。为应对这一挑战，我们首先通过理论分析揭示：混合合成的难负样本会隐式地重新加权用户交互与正负边界之间的相似度差异，从而塑造训练信号。受此启发，我们提出了一种名为双上下文感知负采样（Dual Context-Aware Negative Sampling, DCANS）的新策略。该策略通过评估每个正样本与用户兴趣上下文的对齐程度来增强正样本，同时根据合成负样本与同一兴趣上下文的相关性调整其难度。这一策略将训练方向优化至用户的真实偏好，在保留难负采样优势的同时减轻了假阳性的负面影响。在三个基准数据集上的大量实验表明，我们的方法相较于现有最优基线取得了持续改进。我们的PyTorch实现已公开于https://github.com/Wu-Xi/DCANS。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Negative sampling plays a critical role in collaborative filtering (CF), as it accelerates convergence and improves recommendation accuracy. Among recent studies, mixup-based negative sampling has shown promising performance. However, existing methods primarily focus on increasing the similarity between the synthesized negative and the positive item, without considering the false positive issue commonly found in implicit feedback scenarios. Blindly training all positive samples with overly hard negatives can magnify the impact of false positives and hurt recommendation performance. To address this challenge, we first provide a theoretical analysis revealing that mixup-synthesized hard negatives implicitly reweight the similarity difference between the user's interactions and both the positive and negative boundaries, thereby shaping the training signal. Motivated by this, we propose a novel strategy named Dual Context-Aware Negative Sampling (DCANS), which enhances each positive item by assessing its alignment with the user's interest context, and simultaneously adjusts the hardness of synthesized negatives based on their relevance to the same interest context. This strategy optimizes the training direction toward the user's genuine preferences, mitigating the negative impact of false positives while preserving the benefits of hard negative sampling. Extensive experiments on three benchmark datasets demonstrate that our method achieves consistent improvements over state-of-the-art baselines. Our PyTorch implementation is available https://github.com/Wu-Xi/DCANS.

</details>

---

_知识库更新时间：2026-07-12T07:42:44.681854_
