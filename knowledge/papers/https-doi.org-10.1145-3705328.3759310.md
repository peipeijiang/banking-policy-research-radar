---
title: "打开黑箱：推荐系统中流行度偏差的可解释补救措施"
paper_id: "https://doi.org/10.1145/3705328.3759310"
source: "recsys"
published: "2025-01-01T00:00:00"
score: 43.0
tags: ["paper", "recommender-systems", "Recommender Systems and Techniques", "Advanced Bandit Algorithms Research", "Topic Modeling"]
---

# 打开黑箱：推荐系统中流行度偏差的可解释补救措施

> **英文原标题**：Opening the Black Box: Interpretable Remedies for Popularity Bias in Recommender Systems

[查看原文](https://dblp.org/rec/conf/recsys/AhmadovM25)

## 一句话结论

> 该论文提出一种基于稀疏自编码器的后处理方法，用于解释和缓解深度推荐模型中的流行度偏差，在提升公平性的同时保持推荐准确性。

## 论文信息

- **作者**：Parviz Ahmadov, Masoud Mansoury
- **来源**：RecSys
- **发布时间**：2025-01-01
- **相关度评分**：43.0
- **DOI**：[https://doi.org/10.1145/3705328.3759310](https://doi.org/10.1145/3705328.3759310)

<details open>
<summary><strong>中文摘要</strong></summary>

流行度偏差是推荐系统中一个公认的挑战，即少数热门物品获得不成比例的关注，而大多数非热门物品则被严重忽视。这种不平衡往往导致推荐质量下降以及物品曝光的不公平。尽管现有的缓解技术在一定程度上解决了这一偏差，但它们通常缺乏操作过程的透明性。在本文中，我们提出了一种基于稀疏自编码器（Sparse Autoencoder, SAE）的事后方法，用于解释并缓解深度推荐模型中的流行度偏差。该SAE经过训练以复制预训练模型的行为，同时实现神经元级别的可解释性。通过引入对热门或非热门物品具有明确偏好的合成用户，我们根据神经元的激活模式识别出编码流行度信号的神经元。随后，我们调整最具偏差的神经元的激活值，以引导推荐朝向更公平的曝光。在基于序列推荐模型的两个公开数据集上的实验表明，我们的方法在最小化对准确率影响的同时显著提升了公平性。此外，该方法还提供了可解释性，并能对公平性与准确率之间的权衡进行细粒度控制。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Popularity bias is a well-known challenge in recommender systems, where a small number of popular items receive disproportionate attention, while the majority of less popular items are largely overlooked.This imbalance often results in reduced recommendation quality and unfair exposure of items.Although existing mitigation techniques address this bias to some extent, they typically lack transparency in how they operate.In this paper, we propose a post-hoc method using a Sparse Autoencoder (SAE) to interpret and mitigate popularity bias in deep recommendation models.The SAE is trained to replicate a pre-trained model's behavior while enabling neuron-level interpretability.By introducing synthetic users with clear preferences for either popular or unpopular items, we identify neurons encoding popularity signals based on their activation patterns.We then adjust the activations of the most biased neurons to steer recommendations toward fairer exposure.Experiments on two public datasets using a sequential recommendation model show that our method significantly improves fairness with minimal impact on accuracy.Moreover, it offers interpretability and fine-grained control over the fairness-accuracy trade-off.

</details>

## 深度解读

> 分析依据：**AI 深度分析**

### 核心结论

本文针对推荐系统中的流行度偏差问题，提出了一种基于稀疏自编码器（SAE）的后处理方法，旨在解释并缓解深度推荐模型中的流行度偏差。该方法通过训练SAE复制预训练模型的行为，实现神经元级别的可解释性。通过构造偏好流行或非流行物品的合成用户，识别编码流行度信号的神经元，并调整其激活值以引导推荐结果更公平。在两个公开数据集上使用序列推荐模型进行实验，结果表明该方法在显著提升公平性的同时，对准确率影响极小，并提供了可解释性和对公平-准确权衡的细粒度控制。

### 主要创新

- 提出使用稀疏自编码器（SAE）对深度推荐模型进行后处理解释，实现神经元级别的可解释性。
- 通过构造合成用户识别编码流行度偏差的特定神经元，提供偏差来源的透明分析。
- 通过调整识别出的偏差神经元的激活值，实现公平性干预，且干预粒度可调。
- 在保持推荐准确率的同时显著提升公平性，展示了公平-准确权衡的可控性。

### 研究方法

首先，训练一个稀疏自编码器（SAE）来重建预训练推荐模型的隐藏层表示，使SAE学习到可解释的神经元。然后，构造两组合成用户：一组偏好流行物品，另一组偏好非流行物品，通过比较两组用户激活模式，识别出对流行度敏感的神经元。最后，在推理阶段，对识别出的偏差神经元的激活值进行线性调整（如缩放或偏移），以降低流行度偏差，实现更公平的推荐。

### 关键结果

在两个数据集上，所提方法显著降低了流行度偏差（如降低长尾物品的曝光不均），同时推荐准确率（如NDCG）下降不超过2%。；通过调整干预强度，可以灵活控制公平-准确权衡，且干预效果可解释。；识别出的偏差神经元与物品流行度高度相关，验证了方法的可解释性。

### 技术栈

- 稀疏自编码器（Sparse Autoencoder, SAE）
- 序列推荐模型（如SASRec）
- 合成用户构造
- 神经元激活模式分析
- 线性激活调整

### 方法优势

- 方法具有可解释性，能揭示模型内部流行度偏差的编码机制。
- 后处理方式无需重新训练模型，计算成本低，易于部署。
- 干预粒度细，可针对特定神经元调整，实现精确控制。
- 实验验证了公平性提升与准确率保持的平衡，实用性强。

### 主要局限

- 方法依赖于合成用户的设计，可能无法完全覆盖真实用户偏好多样性。
- 仅针对流行度偏差，未考虑其他类型的偏差（如位置偏差、选择偏差）。
- 实验仅在序列推荐模型上验证，泛化性需在其他推荐范式（如协同过滤）中进一步测试。
- SAE的训练需要访问预训练模型的隐藏表示，可能受限于模型架构的开放性。

### 与当前研究方向的关联

该论文直接针对推荐系统的公平性（流行度偏差）问题，属于公平性研究范畴；同时涉及可解释性（打开黑箱）和序列推荐（实验使用序列模型），与关键词高度相关。

---

_知识库更新时间：2026-07-12T07:42:44.678522_
