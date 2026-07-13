---
title: "可解释的多模态对齐方法用于可迁移推荐系统"
paper_id: "https://doi.org/10.1145/3696410.3714733"
source: "www"
published: "2025-01-01T00:00:00"
score: 50.0
tags: ["paper", "recommender-systems", "Recommender Systems and Techniques", "Topic Modeling", "Machine Learning in Healthcare"]
---

# 可解释的多模态对齐方法用于可迁移推荐系统

> **英文原标题**：Explainable Multi-Modality Alignment for Transferable Recommendation

[查看原文](https://dblp.org/rec/conf/www/0004MGZWZZY25) · [Semantic Scholar](https://www.semanticscholar.org/paper/8668bef005e0325dc37237bec5058c8f5c977d06)

## 一句话结论

> 该论文提出了一种可解释的多模态对齐方法（EARec），通过生成式任务将多种模态并行对齐到共享锚点，并组合模型以提升推荐系统的可迁移性和可解释性，实验表明其优于基线方法。

## 论文信息

- **作者**：Shenghao Yang, Weizhi Ma, Zhiqiang Guo, Min Zhang, Haiyang Wu, Junjie Zhai, Chunhui Zhang, Yuekui Yang
- **来源**：WWW
- **发布时间**：2025-01-01
- **相关度评分**：50.0
- **DOI**：[https://doi.org/10.1145/3696410.3714733](https://doi.org/10.1145/3696410.3714733)

<details open>
<summary><strong>中文摘要</strong></summary>

随着多模态建模技术的发展，近期序列推荐系统通过引入跨领域的通用多模态数据（例如文本和图像）来增强可迁移性。现有方法通常采用成对对齐来缓解模态间的差异。然而，这种对齐范式在可解释性、一致性和可扩展性方面存在局限性，导致性能次优。本文提出了一种面向可迁移推荐系统的可解释多模态对齐方法，即EARec。具体而言，我们设计了一个两阶段框架，在源域中实现可解释的模态对齐，并在目标域中基于对齐后的模态表示进行推荐。在第一阶段，我们采用生成式任务将多种模态并行地对齐到一个具有可解释含义的共享锚点（anchor）上。所有模态共享同一锚点以确保方向一致性。此外，我们将行为视为一种独立模态，将任务特定信息整合到对齐框架中。在第二阶段，我们组合第一阶段训练得到的多个物品模态表示模型，以获得一个能够同时理解多种模态的统一模型，从而为目标域中的推荐提供高质量的物品模态表示。得益于并行模态对齐后接模型组合的方法，该框架在扩展新模态方面展现出灵活性。在多个公开数据集上的实验结果表明，EARec优于基线方法，进一步的分析也证明了所提对齐方法的可解释性和可扩展性。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

With the development of multi-modal modeling techniques, recent sequential recommender systems enhance transferability by incorporating cross-domain universal multi-modal data, e.g., text and image. Existing methods typically adopt pairwise alignment to alleviate the gap between modalities. However, this alignment paradigm has limitations on explainability, consistency, and expansibility, resulting in suboptimal performance. This paper proposes a novel Explainable multi-modality Alignment method for transferable Rec ommender systems, i.e., EARec. Specifically, we design a two-stage framework to achieve explainable modality alignment in the source domain and recommendation based on aligned modality representations in the target domain. In the first stage, we adopt a generative task to align various modalities in parallel to a shared anchor with explainable meaning. All modalities share the same anchor to ensure consistent direction. Additionally, we treat behavior as an independent modality to integrate task-specific information into the alignment framework. In the second stage, we compose multiple item modality representation models trained in the first stage to obtain a unified model capable of understanding various modalities simultaneously, thereby providing high-quality item modality representations for recommendations in the target domain. Benefiting from the approach of parallel modality alignment followed by model composition, the framework shows flexibility in expanding new modalities. Experimental results on multiple public datasets demonstrate the superiority of EARec over baselines, and further analyses indicate the explainability and expansibility of the proposed alignment method.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

论文提出一种可解释的生成式多模态对齐方法EARec，用于可迁移推荐系统。针对现有成对对齐方法在可解释性、一致性和可扩展性方面的局限，EARec采用两阶段框架：第一阶段在源域通过生成任务将多种模态并行对齐到共享的可解释锚点（如物品标题），并将行为视为独立模态以融入推荐特定信息；第二阶段组合多个对齐后的多模态大语言模型（MLLM）获得统一模型，为目标域推荐提供高质量物品表示。实验在多个公开数据集上表明EARec优于基线方法，并展示了其可解释性和可扩展性。

### 主要创新

- 提出基于生成式对齐的多模态对齐范式，替代传统成对对齐，提升可解释性、一致性和可扩展性
- 将行为信息作为独立模态纳入对齐框架，融入推荐任务特定信号
- 采用并行对齐后模型组合的策略，支持新模态的灵活扩展
- 引入可调节的模态组合方法，自适应调整不同模态在推荐中的权重

### 研究方法

论文采用两阶段框架：第一阶段，基于多模态大语言模型（MLLM），对每种模态（文本、视觉、行为）分别进行生成式对齐训练，使用相同的生成目标（物品标题）作为锚点，通过自回归生成损失优化；第二阶段，通过模型组合（参数加权合并）将多个对齐后的MLLM整合为统一模型，用于提取物品的多模态表示，并输入序列推荐模型（Transformer）进行下一项预测。

### 关键结果

EARec在Office、Arts、Instruments、Movielens四个数据集上，HR@10和NDCG@10等指标均优于SASRec、UniSRec、MoRec、MISSRec等基线；EARec_TVB（含行为模态）相比EARec_TV（仅文本和视觉）进一步提升性能；消融实验表明每种模态的加入均带来提升；可解释性分析显示生成结果与锚点的RougeL分数与推荐性能正相关。

### 技术栈

- 多模态大语言模型（MLLM）：Vicuna-v1.5
- 视觉编码器：CLIP ViT-L/14 (patch14-336)
- 行为编码器：SASRec预训练物品嵌入
- 高效微调：LoRA (r=128, alpha=256)
- 模型组合：参数加权合并
- 序列推荐：Transformer编码器（2层，2头）
- 优化器：Adam
- 框架：Transformers库、DeepSpeed、RecBole

### 方法优势

- 提出新颖的生成式对齐范式，显著提升多模态对齐的可解释性
- 两阶段框架设计清晰，支持新模态的灵活扩展
- 将行为模态纳入对齐，有效融合推荐任务信息
- 实验充分，在多个数据集上取得一致优势，并进行了详细的可解释性和可扩展性分析

### 主要局限

- 行为模态的对齐训练数据相对不足，可能导致过拟合（如RougeL分数未提升）
- 模型组合时权重选择依赖下游任务验证，可能增加调参成本
- 仅验证了文本、视觉、行为三种模态，更多模态的扩展效果未充分探讨

### 与当前研究方向的关联

论文紧密围绕多模态推荐、可迁移推荐、序列推荐、LLM与推荐系统结合等关键词，提出可解释的多模态对齐方法，属于推荐系统前沿研究，与用户建模、生成式推荐等方向高度相关。

## 代码与复现

- [ysh-1998/EARec](https://github.com/ysh-1998/EARec)：possible，置信度 30，Stars 7

---

_知识库更新时间：2026-07-13T02:41:41.465483_
