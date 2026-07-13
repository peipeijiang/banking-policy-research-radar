---
title: "TourRank: Utilizing Large Language Models for Documents Ranking with a Tournament-Inspired Strategy"
paper_id: "https://doi.org/10.1145/3696410.3714863"
source: "www"
published: "2025-01-01T00:00:00"
score: 26.0
tags: ["paper", "recommender-systems", "Topic Modeling", "Natural Language Processing Techniques", "Advanced Text Analysis Techniques"]
---

# TourRank: Utilizing Large Language Models for Documents Ranking with a Tournament-Inspired Strategy

[查看原文](https://dblp.org/rec/conf/www/0004LZ0MYSMY25) · [ArXiv](https://arxiv.org/abs/2406.11678) · [Semantic Scholar](https://www.semanticscholar.org/paper/0d25d0fadeb9091ea8c8e054c699d852eaf80374)

## 一句话结论

> 论文提出TourRank方法，受体育赛事启发，通过多阶段分组和积分系统解决LLM在文档排序中的输入长度限制、顺序敏感性和成本平衡问题，在TREC DL和BEIR上取得SOTA性能。

## 论文信息

- **作者**：Yiqun Chen, Qi Liu, Yi Zhang, Weiwei Sun, Xinyu Ma, Wei Yang, Daiting Shi, Jiaxin Mao, Dawei Yin
- **来源**：WWW
- **发布时间**：2025-01-01
- **相关度评分**：26.0
- **DOI**：[https://doi.org/10.1145/3696410.3714863](https://doi.org/10.1145/3696410.3714863)

<details open>
<summary><strong>中文摘要</strong></summary>

大型语言模型（Large Language Models, LLMs）日益被应用于零样本文档排序，并取得了令人称赞的结果。然而，LLMs在排序任务中仍面临若干显著挑战：（1）LLMs受限于有限的输入长度，无法同时处理大量文档；（2）输出文档序列受文档输入顺序影响，导致排序结果不一致；（3）在成本与排序性能之间取得平衡颇具挑战。为解决这些问题，我们提出一种名为TourRank¹的新型文档排序方法，其灵感来源于体育赛事（如国际足联世界杯）。具体而言，我们：1）通过引入类似于体育赛事小组赛阶段的多阶段分组策略，克服了输入长度的限制并降低了排序延迟；2）采用积分系统对多个排序结果进行集成，从而提升了排序性能及对输入顺序的鲁棒性。我们在TREC DL数据集和BEIR基准测试上使用不同LLMs对TourRank进行了测试。实验结果表明，TourRank以适中的成本实现了最先进的性能。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Large Language Models (LLMs) are increasingly employed in zero-shot documents ranking, yielding commendable results. However, several significant challenges still persist in LLMs for ranking: (1) LLMs are constrained by limited input length, precluding them from processing a large number of documents simultaneously; (2) The output document sequence is influenced by the input order of documents, resulting in inconsistent ranking outcomes; (3) Achieving a balance between cost and ranking performance is challenging. To tackle these issues, we introduce a novel documents ranking method called TourRank1. which is inspired by the sport tournaments, such as FIFA World Cup. Specifically, we 1) overcome the limitation in input length and reduce the ranking latency by incorporating a multi-stage grouping strategy similar to the parallel group stage of sport tournaments; 2) improve the ranking performance and robustness to input orders by using a points system to ensemble multiple ranking results. We test TourRank with different LLMs on the TREC DL datasets and the BEIR benchmark. The experimental results demonstrate that TourRank delivers state-of-the-art performance at a modest cost.

</details>

---

_知识库更新时间：2026-07-13T01:23:50.736067_
