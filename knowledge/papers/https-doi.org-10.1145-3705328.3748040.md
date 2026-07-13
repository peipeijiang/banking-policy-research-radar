---
title: "我们真的需要专门化吗？评估通用文本嵌入用于零样本推荐和搜索"
paper_id: "https://doi.org/10.1145/3705328.3748040"
source: "recsys"
published: "2025-01-01T00:00:00"
score: 48.0
tags: ["paper", "recommender-systems", "Topic Modeling", "Recommender Systems and Techniques", "Machine Learning in Healthcare"]
---

# 我们真的需要专门化吗？评估通用文本嵌入用于零样本推荐和搜索

> **英文原标题**：Do We Really Need Specialization? Evaluating Generalist Text Embeddings for Zero-Shot Recommendation and Search

[查看原文](https://dblp.org/rec/conf/recsys/AttimonelliBPJS25) · [ArXiv](https://arxiv.org/abs/2507.05006) · [Semantic Scholar](https://www.semanticscholar.org/paper/5247338575ce40db1bbbadaa6f68887debd4d4b2)

## 一句话结论

> 论文证明通用文本嵌入模型（GTEs）在零样本电子商务推荐和搜索中优于专门微调的模型，挑战了领域特化必要性。

## 论文信息

- **作者**：Matteo Attimonelli, Alessandro Bellis, Claudio Pomo, Dietmar Jannach, Eugenio Di Sciascio, Tommaso Di Noia
- **来源**：RecSys
- **发布时间**：2025-01-01
- **相关度评分**：48.0
- **DOI**：[https://doi.org/10.1145/3705328.3748040](https://doi.org/10.1145/3705328.3748040)

<details open>
<summary><strong>中文摘要</strong></summary>

预训练语言模型（Pre-trained Language Models, PLMs）被广泛用于从推荐系统和搜索中的项目元数据中提取语义表示。在序列推荐中，PLMs通过文本元数据增强基于ID的嵌入表示；而在产品搜索中，它们则将项目特征与用户意图对齐。近期研究表明，需要针对任务和领域进行微调以提升表示能力。本文对电子商务应用中的这一假设提出质疑，证明通用文本嵌入模型（Generalist Text Embedding Models, GTEs）在大规模语料库上预训练后，无需专门适配即可保证强大的零样本性能。我们在主流电子商务基准上的实验表明，GTEs在序列推荐和产品搜索中均优于传统模型及微调模型。我们将此归因于其更优越的表示能力——这些模型能将特征更均匀地分布在整个嵌入空间中。最后，我们证明通过聚焦最具信息量的方向（例如通过主成分分析，PCA）来压缩嵌入维度，能有效降低噪声并提升专用模型的性能。为确保可复现性，我们提供了代码仓库：https://github.com/sisinflab/GTE-Zero-Shot-Recsys。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Pre-trained language models (PLMs) are widely used to derive semantic representations from item metadata in recommendation and search.In sequential recommendation, PLMs enhance ID-based embeddings through textual metadata, while in product search, they align item characteristics with user intent.Recent studies suggest task and domain-specific fine-tuning are needed to improve representational power.This paper challenges this assumption for e-commerce applications, showing that Generalist Text Embedding Models (GTEs), pre-trained on large-scale corpora, can guarantee strong zero-shot performance without specialized adaptation.Our experiments on popular e-commerce benchmarks demonstrate that GTEs outperform traditional and fine-tuned models in both sequential recommendation and product search.We attribute this to a superior representational power, as they distribute features more evenly across the embedding space.Finally, we show that compressing embedding dimensions by focusing on the most informative directions (e.g., via PCA) effectively reduces noise and improves the performance of specialized models.To ensure reproducibility, we provide our repository at https://github.com/sisinflab/GTE-Zero-Shot-Recsys.

</details>

## 深度解读

> 分析依据：**摘要分析**

### 核心结论

本文探讨了在电子商务推荐和搜索中，通用文本嵌入模型（GTEs）是否真的需要任务和领域特定的微调。作者通过实验证明，在大规模语料上预训练的GTEs在零样本场景下，其性能优于传统模型和经过微调的专门模型。在序列推荐和产品搜索任务中，GTEs表现出更强的表征能力，特征在嵌入空间中分布更均匀。此外，通过PCA等方法压缩嵌入维度，聚焦于信息量最大的方向，可以有效减少噪声并提升专门模型的性能。论文提供了开源代码以促进可复现性。

### 主要创新

- 挑战了推荐和搜索中需要任务和领域特定微调的主流假设
- 证明通用文本嵌入模型（GTEs）在零样本场景下优于传统和微调模型
- 发现GTEs的特征在嵌入空间中分布更均匀，归因于其更强的表征能力
- 提出通过PCA压缩嵌入维度可减少噪声并提升专门模型性能

### 研究方法

论文使用预训练语言模型（PLMs）作为基础，对比通用文本嵌入模型（GTEs）与经过微调的专门模型在序列推荐和产品搜索任务上的表现。通过实验评估零样本性能，并分析嵌入空间的特征分布。采用PCA等方法压缩嵌入维度，验证其对模型性能的影响。

### 关键结果

GTEs在电子商务基准测试中优于传统模型和微调模型；GTEs的特征在嵌入空间中分布更均匀；通过PCA压缩嵌入维度可提升专门模型的性能

### 技术栈

- 预训练语言模型（PLMs）
- 通用文本嵌入模型（GTEs）
- 主成分分析（PCA）

### 方法优势

- 挑战了领域内普遍假设，具有创新性
- 实验覆盖序列推荐和产品搜索两个任务
- 提供了开源代码，促进可复现性
- 分析了嵌入空间特性，提供了深入见解

### 主要局限

- 论文局限：仅基于摘要，未提供具体数据集、基线模型和实验细节
- 当前证据局限：摘要未披露消融实验、参数设置或失败案例

### 与当前研究方向的关联

论文与序列推荐、LLM与推荐系统结合、生成式推荐等关键词高度相关，因为其研究通用文本嵌入在推荐和搜索中的应用，并挑战了微调的必要性。

## 代码与复现

- [sisinflab/GTE-Zero-Shot-Recsys](https://github.com/sisinflab/GTE-Zero-Shot-Recsys)：official，置信度 100，Stars 1

---

_知识库更新时间：2026-07-12T10:37:28.677374_
