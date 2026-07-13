---
title: "Pinterest工业级推荐中的自回归生成式检索"
paper_id: "https://doi.org/10.1145/3746252.3761439"
source: "cikm"
published: "2025-01-01T00:00:00"
score: 48.0
tags: ["paper", "recommender-systems", "Recommender Systems and Techniques", "Expert finding and Q&A systems", "Topic Modeling"]
---

# Pinterest工业级推荐中的自回归生成式检索

> **英文原标题**：Autoregressive Generative Retrieval for Industrial-Scale Recommendations at Pinterest

[查看原文](https://dblp.org/rec/conf/cikm/AgarwalBBY0025) · [Semantic Scholar](https://www.semanticscholar.org/paper/63ef1fd6e1d52ce98f3e538ab123e8accf427ab7)

## 一句话结论

> 该论文提出了PinRec，一种自回归生成式检索模型，用于工业级推荐系统，通过结果条件生成和多令牌生成平衡性能、多样性和效率，在Pinterest上实现了点击和搜索的显著提升。

## 论文信息

- **作者**：Prabhat Agarwal, Anirudhan Badrinath, Laksh Bhasin, Jaewon Yang, Jiajing Xu, Charles Rosenberg
- **来源**：CIKM
- **发布时间**：2025-01-01
- **相关度评分**：48.0
- **DOI**：[https://doi.org/10.1145/3746252.3761439](https://doi.org/10.1145/3746252.3761439)

<details open>
<summary><strong>中文摘要</strong></summary>

生成式检索方法利用生成式序列建模技术（如Transformer）为推荐系统生成候选项目。这些方法在学术基准测试中展现出令人瞩目的成果，超越了双塔架构等传统检索模型。然而，当前的生成式检索方法缺乏工业级推荐系统所需的可扩展性，且灵活性不足以满足现代系统对多项指标的要求。本报告介绍了PinRec——一种为Pinterest应用场景开发的新型生成式检索模型。PinRec采用结果条件生成机制，使建模者能够指定如何平衡各类结果指标（如保存次数与点击次数），从而有效对齐业务目标与用户探索需求。此外，PinRec集成了多令牌生成技术，在优化生成过程的同时增强输出多样性。实验表明，PinRec能够成功平衡性能、多样性与效率，为使用生成模型的用户带来显著的积极影响。本报告首次深入研究了生成式检索的生产化部署。我们的实验证明，PinRec可成功平衡性能、多样性与效率，带来全站点击量提升2%、搜索转存量提升4%等显著积极影响。据我们所知，本文标志着生成式检索领域的重要里程碑，首次严格研究了在Pinterest规模下实现生成式检索的实践。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Generative retrieval methods utilize generative sequential modeling techniques, such as transformers, to generate candidate items for recommender systems. These methods have demonstrated promising results in academic benchmarks, surpassing traditional retrieval models like two-tower architectures. However, current generative retrieval methods lack the scalability required for industrial recommender systems, and they are insufficiently flexible to satisfy the multiple metric requirements of modern systems. This talk introduces PinRec, a novel generative retrieval model developed for applications at Pinterest. PinRec utilizes outcome-conditioned generation, enabling modelers to specify how to balance various outcome metrics, such as the number of saves and clicks, to effectively align with business goals and user exploration. Additionally, PinRec incorporates multi-token generation to enhance output diversity while optimizing generation. Our experiments demonstrate that PinRec can successfully balance performance, diversity, and efficiency, delivering a significant positive impact to users using generative models. This talk presents the first in-depth study on productionizing generative retrieval. Our experiments demonstrate that PinRec can successfully balance performance, diversity, and efficiency, delivering a significant positive impact such as +2% sitewide clicks and +4% search repins. This paper marks a significant milestone in generative retrieval, as it presents, to our knowledge, the first rigorous study on implementing generative retrieval at the scale of Pinterest.

</details>

## 深度解读

> 分析依据：**摘要分析**

### 核心结论

本文介绍了PinRec，一种为Pinterest应用开发的新型生成式检索模型。该模型利用条件生成技术，允许建模者指定如何平衡不同结果指标（如保存数和点击数），以有效对齐业务目标和用户探索。此外，PinRec采用多令牌生成来增强输出多样性并优化生成过程。实验表明，PinRec能够成功平衡性能、多样性和效率，为使用生成模型的用户带来显著的正面影响，例如全站点击量增加2%，搜索重钉增加4%。本文是首个对生成式检索进行工业化深度研究的工作，标志着在Pinterest规模上实现生成式检索的重要里程碑。

### 主要创新

- 提出结果条件生成（outcome-conditioned generation），允许建模者指定如何平衡多种结果指标以对齐业务目标。
- 引入多令牌生成（multi-token generation）以增强输出多样性并优化生成。
- 首次在工业规模（Pinterest）上对生成式检索进行深入研究并成功部署。

### 研究方法

摘要未提供具体技术路线，但提及使用生成式序列建模技术（如Transformer）和条件生成方法。

### 关键结果

PinRec成功平衡了性能、多样性和效率。；全站点击量增加2%。；搜索重钉增加4%。

### 技术栈

- 摘要未提供具体算法、工具或数学方法。

### 方法优势

- 首次在工业规模上实现生成式检索，具有实际应用价值。
- 提出条件生成方法，灵活平衡多种业务指标。
- 多令牌生成提升了输出多样性。

### 主要局限

- 摘要未提供局限性信息。当前证据局限：仅基于摘要，无法评估完整论文的局限性。

### 与当前研究方向的关联

与生成式推荐、序列推荐、工业落地高度相关，涉及推荐系统的性能、多样性和效率平衡。

---

_知识库更新时间：2026-07-12T10:37:28.678286_
