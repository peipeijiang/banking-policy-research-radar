---
title: "通用物品标记化用于可迁移生成式推荐"
paper_id: "https://doi.org/10.1145/3805712.3809720"
source: "openalex"
published: "2026-07-10T00:00:00"
score: 53.0
tags: ["paper", "recommender-systems", "Multimodal Machine Learning Applications", "Generative Adversarial Networks and Image Synthesis", "Topic Modeling"]
---

# 通用物品标记化用于可迁移生成式推荐

> **英文原标题**：Universal Item Tokenization for Transferable Generative Recommendation

[查看原文](https://doi.org/10.1145/3805712.3809720) · [ArXiv](https://arxiv.org/abs/2504.04405)

## 一句话结论

> 提出一种通用物品分词方法，将物品表示为可迁移的代码序列，使生成式推荐模型能够跨域转移，解决了现有方法领域特定、难以迁移的问题。

## 论文信息

- **作者**：Bowen Zheng, Hongyu Lu, Yu Chen, Wayne Xin Zhao, Ji-Rong Wen
- **来源**：Proceedings of the 49th International ACM SIGIR Conference on Research and Development in Information Retrieval
- **发布时间**：2026-07-10
- **相关度评分**：53.0
- **DOI**：[https://doi.org/10.1145/3805712.3809720](https://doi.org/10.1145/3805712.3809720)

<details open>
<summary><strong>中文摘要</strong></summary>

近年来，生成式推荐（generative recommendation）作为一种前景广阔的新范式出现，吸引了大量研究关注。其基本框架包括一个物品分词器（item tokenizer），该分词器将每个物品表示为一串代码序列作为其标识符，以及一个生成式推荐器（generative recommender），通过自回归生成目标物品标识符来预测下一个物品。然而，在现有方法中，分词器和推荐器通常都是领域特定的（domain-specific），这限制了它们有效迁移或适应新领域的能力。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Recently, generative recommendation has emerged as a promising paradigm, attracting significant research attention. The basic framework involves an item tokenizer, which represents each item as a sequence of codes serving as its identifier, and a generative recommender that predicts the next item by autoregressively generating the target item identifier. However, in existing methods, both the tokenizer and the recommender are typically domain-specific, limiting their ability for effective transfer or adaptation to new domains.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

本文提出UTGRec，一种通用物品标记化方法，旨在实现可迁移的生成式推荐。现有方法通常针对特定领域，限制了跨域迁移能力。UTGRec利用多模态大语言模型（MLLM）编码物品内容，并通过树状码本进行表示离散化。为有效学习通用标记器，引入双轻量解码器重建文本和图像以捕获内容知识，并通过共现对齐与重建整合协同信号。最后，提出联合学习框架预训练和适配可迁移生成式推荐器。在四个公开数据集上的实验表明，UTGRec优于传统和生成式推荐基线。

### 主要创新

- 提出通用物品标记化框架，利用多模态内容实现跨域可迁移生成式推荐。
- 设计树状码本结构，通过前缀残差操作和共享叶码本增强多域语义融合。
- 引入双轻量解码器（文本和图像）进行原始内容重建，结合扩散损失优化图像重建。
- 通过共现物品对齐和重建整合协同知识，提升标记器的推荐能力。
- 提出两阶段微调策略，固定码本矩阵仅更新投影矩阵以保留通用知识。

### 研究方法

采用Qwen2-VL作为MLLM编码物品文本和图像，通过提示模板压缩为L个表示。应用前缀残差操作得到基础表示和增量表示，利用树状码本（根码本和共享叶码本）进行离散化。使用双轻量Transformer解码器重建文本（MLM损失）和图像（扩散损失）。通过对比学习对齐共现物品表示，并通过重建正样本物品内容整合协同信号。联合优化码本损失、内容重建损失、对齐损失和重建损失。预训练生成式推荐器（T5）后，在下游领域微调标记器（仅更新投影矩阵）和推荐器。

### 关键结果

在四个下游数据集（Instrument、Scientific、Game、Office）上，UTGRec在所有指标（Recall@5/10, NDCG@5/10）上均优于所有基线，包括传统、基于内容和生成式推荐器。消融实验表明，树状码本、协同对齐与重建、标记器微调和推荐器预训练均贡献显著。模型扩展性分析显示，UTGRec随模型层数增加性能持续提升，而基线易过拟合。长尾物品分析中，UTGRec在所有流行度组别均优于基线，尤其在冷启动物品上优势明显。

### 技术栈

- Qwen2-VL (MLLM)
- LoRA (低秩微调)
- 树状码本 (根码本+叶码本)
- 前缀残差操作
- 双轻量Transformer解码器
- 扩散损失 (DiffLoss)
- InfoNCE对比损失
- T5 (生成式推荐器)
- AdamW优化器
- 余弦学习率调度

### 方法优势

- 首次提出通用物品标记化方法，实现跨域可迁移生成式推荐。
- 充分利用多模态内容（文本和图像），通过MLLM编码和双解码器重建。
- 树状码本设计有效缓解多域码本坍塌，提升语义融合。
- 协同知识整合（对齐与重建）增强了标记器的推荐相关性。
- 实验充分，在多个数据集上显著优于基线，并进行了详细的消融和扩展性分析。

### 主要局限

- 依赖MLLM，计算资源需求较高。
- 仅考虑文本和图像，未利用其他模态（如音频、视频）。
- 协同知识整合仅基于共现假设，可能引入噪声。
- 微调策略需针对每个新域调整，效率有待提升。

### 与当前研究方向的关联

论文直接涉及生成式推荐、序列推荐、多模态推荐和迁移学习，与LLM结合推荐（使用MLLM）高度相关，同时涉及物品标记化和协同信号整合，对推荐系统的工业落地有参考价值。

---

_知识库更新时间：2026-07-12T10:37:28.676254_
