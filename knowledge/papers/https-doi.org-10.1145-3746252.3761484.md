---
title: "RerankArena: A Unified Platform for Evaluating Retrieval, Reranking and RAG with Human and LLM Feedback"
paper_id: "https://doi.org/10.1145/3746252.3761484"
source: "cikm"
published: "2025-01-01T00:00:00"
score: 10.0
tags: ["paper", "recommender-systems", "Information Retrieval and Search Behavior", "Multimodal Machine Learning Applications", "Topic Modeling"]
---

# RerankArena: A Unified Platform for Evaluating Retrieval, Reranking and RAG with Human and LLM Feedback

[查看原文](https://dblp.org/rec/conf/cikm/AbdallahAPMAJ25) · [ArXiv](https://arxiv.org/abs/2508.05512) · [Semantic Scholar](https://www.semanticscholar.org/paper/14d2d1dc16d8ab214e2daf9698c457499d8dff44)

## 一句话结论

> 该论文提出了RerankArena，一个统一平台，通过人类和LLM反馈来评估检索、重排序和RAG系统的性能。

## 论文信息

- **作者**：Abdelrahman Abdallah, Mahmoud Abdalla, Bhawna Piryani, Jamshid Mozafari, Mohammed M. Abdelgwad, Adam Jatowt
- **来源**：CIKM
- **发布时间**：2025-01-01
- **相关度评分**：10.0
- **DOI**：[https://doi.org/10.1145/3746252.3761484](https://doi.org/10.1145/3746252.3761484)

<details open>
<summary><strong>中文摘要</strong></summary>

评估检索增强生成（RAG）与文档重排序系统的质量仍具挑战性，主要缺乏可扩展、以用户为中心且多视角的评估工具。我们提出RankArena，一个统一平台，通过结构化的人类与基于大语言模型（LLM）的反馈，对检索流程、重排序器及RAG系统进行性能比较与分析，并支持此类反馈的收集。RankArena支持多种评估模式：直接重排序可视化、基于人类或LLM投票的盲法成对比较、有监督的手动文档标注，以及端到端的RAG答案质量评估。该平台通过成对偏好与全列表标注两种方式捕获细粒度相关性反馈，同时记录辅助元数据，如移动指标、标注时间与质量评分。平台还集成了LLM-as-a-judge评估功能，支持模型生成排序与人类真实标注之间的对比。所有交互均存储为结构化评估数据集，可用于训练重排序器、奖励模型、判断智能体或检索策略选择器。我们的平台已公开访问，网址为https://rankarena.ngrok.io/，并附有演示视频：https://youtu.be/jIYAP4PaSSI。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Evaluating the quality of retrieval-augmented generation (RAG) and document reranking systems remains challenging due to the lack of scalable, user-centric, and multi-perspective evaluation tools. We introduce RankArena, a unified platform for comparing and analysing the performance of retrieval pipelines, rerankers, and RAG systems using structured human and LLM-based feedback as well as for collecting such feedback. RankArena supports multiple evaluation modes: direct reranking visualisation, blind pairwise comparisons with human or LLM voting, supervised manual document annotation, and end-to-end RAG answer quality assessment. It captures fine-grained relevance feedback through both pairwise preferences and full-list annotations, along with auxiliary metadata such as movement metrics, annotation time, and quality ratings. The platform also integrates LLM-as-a-judge evaluation, enabling comparison between model-generated rankings and human ground truth annotations. All interactions are stored as structured evaluation datasets that can be used to train rerankers, reward models, judgment agents, or retrieval strategy selectors. Our platform is publicly available at https://rankarena.ngrok.io/, and the Demo video is provided. https://youtu.be/jIYAP4PaSSI.

</details>

---

_知识库更新时间：2026-07-12T10:37:28.678127_
