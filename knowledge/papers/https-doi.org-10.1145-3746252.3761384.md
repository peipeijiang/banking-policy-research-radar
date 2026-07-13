---
title: "Autonomous Reasoning-Retrieval for Large Language Model Based Recommendation"
paper_id: "https://doi.org/10.1145/3746252.3761384"
source: "cikm"
published: "2025-01-01T00:00:00"
score: 64.0
tags: ["paper", "recommender-systems", "Recommender Systems and Techniques", "Sentiment Analysis and Opinion Mining", "Multimodal Machine Learning Applications"]
---

# Autonomous Reasoning-Retrieval for Large Language Model Based Recommendation

[查看原文](https://dblp.org/rec/conf/cikm/000500WLCZW25) · [Semantic Scholar](https://www.semanticscholar.org/paper/4da3ff3d0db1d215e33514a97a47d401a039e35a)

## 一句话结论

> 提出DeepRec，通过强化学习优化LLM与传统推荐模型的多轮交互，实现深度物品空间探索，显著提升推荐性能。

## 论文信息

- **作者**：Bowen Zheng, Xiaolei Wang, Enze Liu, Xi Wang, Hongyu Lu, Yu Chen, Wayne Xin Zhao, Ji-Rong Wen
- **来源**：CIKM
- **发布时间**：2025-01-01
- **相关度评分**：64.0
- **DOI**：[https://doi.org/10.1145/3746252.3761384](https://doi.org/10.1145/3746252.3761384)

<details open>
<summary><strong>中文摘要</strong></summary>

近年来，大语言模型（LLMs）已被引入推荐系统（RSs），用作推荐主干或增强传统推荐模型（TRMs）。然而，现有的基于LLM的推荐系统未能充分利用LLMs（如世界知识与推理能力）与TRMs（如推荐特定知识与计算效率）的互补优势，导致对物品空间的探索较为浅层。为解决这一局限，我们提出DeepRec，一种新颖的基于LLM的推荐方法，它促进LLMs与TRMs之间自主的多轮交互，以实现对物品空间的深度探索。在每一轮交互中，LLMs对用户偏好进行推理，并与TRMs协作检索候选物品。经过多轮交互后，LLMs对聚合后的候选物品进行排序，生成最终推荐。我们利用强化学习（RL）进行优化，并在三个关键方面做出创新贡献：基于推荐模型的数据展开、面向推荐的分层奖励，以及两阶段RL训练策略。在数据展开方面，我们设计了一种偏好感知的TRM，LLMs与之交互以构建轨迹数据。在奖励设计方面，我们提出了一种分层奖励函数，包含过程级奖励和结果级奖励，分别用于优化交互过程和推荐质量。在RL训练方面，我们的两阶段RL策略首先引导LLMs学习与TRMs的有效交互，随后进行面向推荐的RL以提升性能。在公开数据集上的实验表明，DeepRec显著优于传统及现有基于LLM的基线方法，为推荐系统中的深度探索建立了新范式。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Recently, large language models (LLMs) have been introduced into recommender systems (RSs) as recommendation backbones or to enhance traditional recommendation models (TRMs). However, existing LLM-based RSs fail to fully leverage the complementary strengths of LLMs (e.g., world knowledge and reasoning capabilities) and TRMs (e.g., recommendation-specific knowledge and computational efficiency), resulting in shallow exploration of the item space. To address this limitation, we propose DeepRec, a novel LLM-based RS approach that facilitates autonomous multi-turn interactions between LLMs and TRMs for deep item space exploration. In each interaction turn, LLMs reason over user preferences and collaborate with TRMs to retrieve candidate items. After multi-turn interaction, LLMs rank the aggregated candidates to generate the final recommendations. We utilize reinforcement learning (RL) for optimization and introduce novel contributions in three key aspects: recommendation model based data rollout, recommendation-oriented hierarchical rewards, and a two-stage RL training strategy. For data rollout, we design a preference-aware TRM, with which LLMs interact to construct trajectory data. For reward design, we propose a hierarchical reward function that comprises both process-level and outcome-level rewards to optimize the interaction process and recommendation quality, respectively. For RL training, our two-stage RL strategy first guides LLMs to learn effective interactions with TRMs, followed by recommendation-oriented RL for performance enhancement. Experiments on public datasets show that DeepRec substantially outperforms both traditional and existing LLM-based baselines, establishing a new paradigm for deep exploration in recommender systems.

</details>

---

_知识库更新时间：2026-07-12T07:42:44.679031_
