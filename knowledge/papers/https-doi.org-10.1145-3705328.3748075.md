---
title: "利用大语言模型增强序列推荐器以实现视频与评论联合推荐"
paper_id: "https://doi.org/10.1145/3705328.3748075"
source: "recsys"
published: "2025-01-01T00:00:00"
score: 66.0
tags: ["paper", "recommender-systems", "Recommender Systems and Techniques", "Topic Modeling", "Sentiment Analysis and Opinion Mining"]
---

# 利用大语言模型增强序列推荐器以实现视频与评论联合推荐

> **英文原标题**：Enhancing Sequential Recommender with Large Language Models for Joint Video and Comment Recommendation

[查看原文](https://dblp.org/rec/conf/recsys/0005L0YBLLZW25) · [ArXiv](https://arxiv.org/abs/2403.13574) · [Semantic Scholar](https://www.semanticscholar.org/paper/db27dd3ac801d641059ba335a4d7ff70b1bab478)

## 一句话结论

> 该论文提出利用大语言模型增强序列推荐系统，以联合推荐视频和评论，通过融合多模态信息提升推荐效果。

## 论文信息

- **作者**：Bowen Zheng, Zihan Lin, Enze Liu, Chen Yang, Enyang Bai, Cheng Ling, Han Li, Wayne Xin Zhao, Ji-Rong Wen
- **来源**：RecSys
- **发布时间**：2025-01-01
- **相关度评分**：66.0
- **DOI**：[https://doi.org/10.1145/3705328.3748075](https://doi.org/10.1145/3705328.3748075)

<details open>
<summary><strong>中文摘要</strong></summary>

本文提出LSVCR框架，用于在线视频平台中联合进行视频和评论推荐。现有推荐系统主要关注用户与视频的交互行为，忽略了评论内容及交互在用户偏好建模中的作用。LSVCR包含两个核心组件：序列推荐（SR）模型作为部署时的主骨干，以及大语言模型（LLM）作为训练时的补充推荐器（部署时丢弃）。通过两阶段训练范式整合两者优势：第一阶段进行个性化偏好对齐，对齐SR模型与LLM的偏好表示；第二阶段进行面向推荐的微调。在快手工业数据集和Amazon基准上的实验表明，LSVCR在视频和评论推荐任务上均优于基线。在线A/B测试中，评论观看时长提升4.13%。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Nowadays, reading or writing comments on captivating videos has emerged as a critical part of the viewing experience on online video platforms. However, existing recommender systems primarily focus on users' interaction behaviors with videos, neglecting comment content and interaction in user preference modeling. In this paper, we propose a novel recommendation approach called LSVCR that utilizes user interaction histories with both videos and comments to jointly perform personalized video and comment recommendation. Specifically, our approach comprises two key components: sequential recommendation (SR) model and supplemental large language model (LLM) recommender. The SR model functions as the primary recommendation backbone (retained in deployment) of our method for efficient user preference modeling. Concurrently, we employ a LLM as the supplemental recommender (discarded in deployment) to better capture underlying user preferences derived from heterogeneous interaction behaviors. In order to integrate the strengths of the SR model and the supplemental LLM recommender, we introduce a two-stage training paradigm. The first stage, personalized preference alignment, aims to align the preference representations from both components, thereby enhancing the semantics of the SR model. The second stage, recommendation-oriented fine-tuning, involves fine-tuning the alignment-enhanced SR model according to specific objectives. Extensive experiments in both video and comment recommendation tasks demonstrate the effectiveness of LSVCR. Moreover, online A/B testing on KuaiShou platform verifies the practical benefits of our approach. In particular, we attain a cumulative gain of 4.13% in comment watch time.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

本文提出LSVCR框架，用于在线视频平台中联合进行视频和评论推荐。现有推荐系统主要关注用户与视频的交互行为，忽略了评论内容及交互在用户偏好建模中的作用。LSVCR包含两个核心组件：序列推荐（SR）模型作为部署时的主骨干，以及大语言模型（LLM）作为训练时的补充推荐器（部署时丢弃）。通过两阶段训练范式整合两者优势：第一阶段进行个性化偏好对齐，对齐SR模型与LLM的偏好表示；第二阶段进行面向推荐的微调。在快手工业数据集和Amazon基准上的实验表明，LSVCR在视频和评论推荐任务上均优于基线。在线A/B测试中，评论观看时长提升4.13%。

### 主要创新

- 提出联合视频和评论推荐的框架LSVCR，同时建模视频和评论交互历史。
- 设计两阶段训练范式：个性化偏好对齐和面向推荐的微调，有效整合SR模型与LLM的优势。
- 引入序列-补充偏好对比和视频-评论偏好对比两种对齐损失，增强SR模型的语义。
- 采用随机位置编码技术，解决对齐阶段序列长度受限问题。

### 研究方法

LSVCR由SR模型和补充LLM推荐器组成。SR模型使用LLM编码视频标题和评论作为文本特征，通过Transformer建模序列，并利用交叉融合编码器整合视频和评论序列。补充LLM推荐器将用户交互历史格式化为指令，通过LLM生成增强偏好表示。第一阶段通过序列-补充偏好对比和视频-评论偏好对比对齐两者表示，并联合优化LLM生成损失和SR对比损失。第二阶段丢弃LLM，加入ID嵌入，通过ID-文本正则化和任务特定对比损失微调SR模型。

### 关键结果

在快手工业数据集上，视频推荐Recall@10达0.3322，NDCG@10达0.2233；评论推荐Recall@10达0.3901，NDCG@10达0.2541。在线A/B测试中，评论观看时长提升4.1264%，交互数提升1.3557%。在Amazon数据集上，LSVCR w/o Comment也优于所有基线。

### 技术栈

- ChatGLM3 (LLM)
- LoRA (低秩适应)
- Transformer
- 多头注意力 (MHA)
- 加性注意力 (Additive Attention)
- InfoNCE损失
- AdamW优化器
- 随机位置编码

### 方法优势

- 创新性地联合建模视频和评论交互，提升推荐质量。
- 两阶段训练范式有效结合LLM的语义理解能力和SR模型的高效性。
- 在工业数据集和在线A/B测试中均取得显著提升，验证了实用性。
- 消融实验和泛化性分析全面，证明了各模块的有效性。

### 主要局限

- 依赖LLM进行离线编码和训练，计算成本较高。
- 评论推荐任务中候选集仅限当前视频下的评论，可能限制多样性。
- 未探讨不同LLM规模对性能的影响。

### 与当前研究方向的关联

论文高度相关于序列推荐、LLM与推荐系统结合、用户建模、工业落地等关键词。它提出了序列推荐与LLM结合的新范式，并针对视频和评论推荐场景进行用户建模，最终在工业平台验证。

---

_知识库更新时间：2026-07-12T07:42:44.678239_
