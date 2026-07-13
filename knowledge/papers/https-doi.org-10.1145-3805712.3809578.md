---
title: "从预训练和协同信号中学习分解的上下文令牌表示用于生成式推荐"
paper_id: "https://doi.org/10.1145/3805712.3809578"
source: "openalex"
published: "2026-07-10T00:00:00"
score: 63.0
tags: ["paper", "recommender-systems", "Video Analysis and Summarization", "Recommender Systems and Techniques", "Image Retrieval and Classification Techniques"]
---

# 从预训练和协同信号中学习分解的上下文令牌表示用于生成式推荐

> **英文原标题**：Learning Decomposed Contextual Token Representations from Pretrained and Collaborative Signals for Generative Recommendation

[查看原文](https://doi.org/10.1145/3805712.3809578) · [ArXiv](https://arxiv.org/abs/2509.10468)

## 一句话结论

> 提出DECOR框架，通过分解的上下文token表示融合预训练语义和协同信号，解决生成式推荐中目标不一致问题，在三个数据集上超越基线。

## 论文信息

- **作者**：Yifan Liu, Yaokun Liu, Zelin Li, Zhenrui Yue, Gyuseok Lee, Ruichen Yao, Yang Zhang
- **来源**：Proceedings of the 49th International ACM SIGIR Conference on Research and Development in Information Retrieval
- **发布时间**：2026-07-10
- **相关度评分**：63.0
- **DOI**：[https://doi.org/10.1145/3805712.3809578](https://doi.org/10.1145/3805712.3809578)

<details open>
<summary><strong>中文摘要</strong></summary>

近期，生成式推荐系统采用了一种两阶段范式：首先利用预训练分词器将物品分词为语义ID，随后训练大型语言模型（LLMs）通过序列到序列建模生成下一个物品。然而，这两个阶段的优化目标并不一致：分词器预训练阶段侧重于语义重建，而推荐模型训练阶段则聚焦于用户交互建模。这种目标错位导致了两个关键局限：（i）次优的静态分词，即固定的分词分配无法反映多样化的使用情境；（ii）预训练语义被丢弃，即预训练知识（通常来自语言模型嵌入）在基于用户交互的推荐训练过程中被覆盖。为解决上述局限，我们提出学习分解式上下文令牌表示（DECOR），这是一个统一框架，能够在保留预训练语义的同时增强令牌嵌入的适应性。DECOR引入了上下文感知的令牌组合机制，以根据用户交互上下文优化令牌嵌入，并采用分解式嵌入融合方法，将预训练码本嵌入与新学习的协同嵌入进行整合。在三个真实世界数据集上的实验表明，DECOR在推荐性能上持续优于最先进的基线模型。我们的代码已开源至 https://github.com/yliuaa/DECOR.git。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Recent advances in generative recommenders adopt a two-stage paradigm: items are first tokenized into semantic IDs using a pretrained tokenizer, and then large language models (LLMs) are trained to generate the next item via sequence-to-sequence modeling. However, these two stages are optimized for different objectives: semantic reconstruction during tokenizer pretraining versus user interaction modeling during recommender training. This objective misalignment leads to two key limitations: (i) suboptimal static tokenization, where fixed token assignments fail to reflect diverse usage contexts; and (ii) discarded pretrained semantics, where pretrained knowledge—typically from language model embeddings—is overwritten during recommender training on user interactions. To address these limitations, we propose to learn DEcomposed COntextual Token Representations (DECOR), a unified framework that preserves pretrained semantics while enhancing the adaptability of token embeddings. DECOR introduces contextualized token composition to refine token embeddings based on user interaction context, and decomposed embedding fusion that integrates pretrained codebook embeddings with newly learned collaborative embeddings. Experiments on three real-world datasets demonstrate that DECOR consistently outperforms state-of-the-art baselines in recommendation performance. Our code is available at https://github.com/yliuaa/DECOR.git.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

本文针对生成式推荐中两阶段范式（预训练分词器+LLM推荐器）的目标不一致问题，提出DECOR框架。该框架通过分解嵌入融合（保留预训练语义嵌入并融合可学习的协同嵌入）和上下文令牌组合（根据用户交互历史动态调整静态令牌嵌入）两个模块，解决了静态分词导致的表示瓶颈和预训练语义被丢弃的问题。在三个真实数据集上的实验表明，DECOR在推荐性能上持续优于现有基线，且收敛速度更快。

### 主要创新

- 首次明确分析静态分词如何限制生成式推荐器适应不同用户上下文的能力。
- 提出分解嵌入融合，将冻结的预训练语义嵌入与可学习的协同嵌入动态融合。
- 提出上下文令牌组合，通过注意力机制基于用户历史动态调整输入令牌嵌入。
- 引入可学习的BOS查询向量，作为高层语义锚点以增强初始令牌生成的上下文对齐。

### 研究方法

采用两阶段生成式推荐范式：首先使用RQ-VAE对预训练语义嵌入进行量化得到语义ID，然后训练T5模型进行自回归生成。DECOR在推荐器训练阶段集成两个模块：分解嵌入融合通过投影和融合层整合预训练代码本嵌入与协同嵌入；上下文令牌组合通过注意力池化从历史序列提取上下文向量，并基于该向量对候选令牌集进行软组合，最后通过残差连接与静态嵌入融合。

### 关键结果

在Scientific、Instrument、Game三个数据集上，DECOR在Recall@5/10和NDCG@5/10上均优于所有基线。相比最强基线，NDCG@10相对提升在Scientific上超过14%，在Instrument上约5%，在Game上约3%。

### 技术栈

- RQ-VAE
- T5
- Sentence-T5
- 注意力机制
- 残差连接
- 层归一化
- 多层感知机

### 方法优势

- 方法创新性强，同时解决静态分词和预训练语义丢失两个关键问题。
- 实验充分，在三个数据集上全面对比多种基线，包括传统和生成式方法。
- 消融实验验证了各模块的有效性。
- 复杂度分析表明额外开销可控。

### 主要局限

- 仅使用Amazon Review数据集，未在更多领域验证泛化性。
- 上下文令牌组合的候选集大小固定，可能限制灵活性。
- 未讨论对冷启动物品的详细效果。

### 与当前研究方向的关联

论文聚焦生成式推荐和序列推荐，提出结合预训练语义与协同信号的方法，与LLM与推荐系统结合、用户建模高度相关。

## 代码与复现

- [yliuaa/DECOR](https://github.com/yliuaa/DECOR)：possible，置信度 30，Stars 3

---

_知识库更新时间：2026-07-12T10:37:28.676061_
