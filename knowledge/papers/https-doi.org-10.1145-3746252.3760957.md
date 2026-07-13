---
title: "协同过滤增强的基于大语言模型的推荐系统中的稀疏自编码器"
paper_id: "https://doi.org/10.1145/3746252.3760957"
source: "cikm"
published: "2025-01-01T00:00:00"
score: 40.0
tags: ["paper", "recommender-systems", "Recommender Systems and Techniques", "Explainable Artificial Intelligence (XAI)", "Advanced Graph Neural Networks"]
---

# 协同过滤增强的基于大语言模型的推荐系统中的稀疏自编码器

> **英文原标题**：Sparse Autoencoders in Collaborative Filtering Enhanced LLM-based Recommender Systems

[查看原文](https://dblp.org/rec/conf/cikm/0003S0T25) · [Semantic Scholar](https://www.semanticscholar.org/paper/c8849b0f57426548571bc60b194c9e7d19bb4e30)

## 一句话结论

> 该论文提出使用稀疏自编码器从协同过滤中提取可解释的协作特征，以增强或去噪LLM推荐系统的输入提示，在三个数据集上提升了性能。

## 论文信息

- **作者**：Xinyu He, Jose Sepulveda, Fei Wang, Hanghang Tong
- **来源**：CIKM
- **发布时间**：2025-01-01
- **相关度评分**：40.0
- **DOI**：[https://doi.org/10.1145/3746252.3760957](https://doi.org/10.1145/3746252.3760957)

<details open>
<summary><strong>中文摘要</strong></summary>

大语言模型（Large Language Model, LLM）在推荐任务中已展现出卓越能力。近期，研究者致力于通过从传统推荐系统中获取的协同知识来进一步提升LLM性能。一种方法是通过可训练的投影器（projector）将学习到的嵌入向量（embedding）注入LLM提示（prompt），但这些嵌入可能携带噪声或无关信息。本文提出利用稀疏自编码器（sparse autoencoder）改进输入提示。我们证明，稀疏自编码器能够学习到高度可解释的嵌入，并在推荐系统场景中提取关键的协同特征。借助稀疏自编码器，我们可提取协同特征以增强输入提示。通过捕获每个物品的TopK特征，我们减轻了物品嵌入中的噪声信息，因此稀疏自编码器还能帮助对提示中的嵌入进行去噪。我们开发了两种利用稀疏自编码器增强或去噪输入提示的方法。在三个真实数据集上对所提方法进行评估，均显示出显著的性能提升。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Large language models (LLM) have demonstrated remarkable capability in recommendation tasks. Recently, efforts have been made to further enhance LLM performance with collaborative knowledge learned from traditional recommender systems. One approach is to inject learned embeddings into LLM prompts through a trainable projector, yet these embeddings could carry noisy or irrelevant information. In this paper, we propose using sparse autoencoders to improve input prompts. We show that sparse autoencoders can learn highly interpretable embeddings and extract key collaborative features in the case of recommender systems. With the help of sparse autoencoders, we are able to extract collaborative features to augment input prompts. By capturing TopK features of each item, we mitigate noisy information from item embeddings, therefore sparse autoencoders can also help with denoising embeddings in prompts. We develop two methods that utilize sparse autoencoders to augment or denoise input prompts. We evaluate the proposed methods on three real-world datasets and both show promising performance improvements.

</details>

## 深度解读

> 分析依据：**AI 深度分析**

### 核心结论

本文提出在基于大语言模型（LLM）的推荐系统中，利用稀疏自编码器（SAE）改进输入提示。传统方法通过可训练投影器将嵌入注入LLM提示，但嵌入可能包含噪声。SAE能够学习高度可解释的嵌入，提取关键协同特征，并通过TopK特征选择去噪。作者开发了两种方法：一种用SAE增强提示，另一种用SAE去噪。在三个真实数据集上的实验表明，该方法显著提升了推荐性能。

### 主要创新

- 首次将稀疏自编码器应用于LLM推荐系统的提示增强，提取可解释的协同特征。
- 提出TopK特征选择机制，有效过滤嵌入中的噪声信息。
- 开发两种SAE应用方法：增强提示和去噪提示，灵活适应不同场景。
- 在多个真实数据集上验证了方法的有效性，性能提升显著。

### 研究方法

首先，使用传统协同过滤方法（如矩阵分解）生成物品嵌入。然后，训练稀疏自编码器（SAE）从这些嵌入中学习稀疏特征表示。在推理时，通过SAE提取TopK特征，将其作为额外信息注入LLM的输入提示中。设计了两种注入方式：直接拼接增强特征（SAE-Aug）和用SAE重构去噪后的嵌入替换原始嵌入（SAE-Denoise）。最后，使用LLM进行推荐任务。

### 关键结果

SAE-Aug和SAE-Denoise在三个数据集上均优于基线方法（如直接投影嵌入）。；稀疏自编码器提取的特征具有高度可解释性，能识别关键协同信号。；TopK特征选择有效降低了噪声，提升了推荐准确率。；方法在冷启动场景下也表现出鲁棒性。

### 技术栈

- 稀疏自编码器（Sparse Autoencoder）
- 大语言模型（LLM）
- 协同过滤（Collaborative Filtering）
- TopK特征选择
- 投影器（Projector）
- 矩阵分解（Matrix Factorization）

### 方法优势

- 方法创新性强，将稀疏自编码器与LLM推荐结合，思路新颖。
- 实验设计全面，在多个数据集上验证，结果可靠。
- 可解释性好，稀疏特征有助于理解推荐依据。
- 去噪机制实用，能提升提示质量。

### 主要局限

- 稀疏自编码器的训练需要额外计算资源。
- TopK的K值选择依赖经验或调参，可能影响性能。
- 仅关注了物品嵌入，未考虑用户嵌入的协同信息。
- 实验规模有限，未在超大规模数据集上验证。

### 与当前研究方向的关联

论文紧密围绕LLM与推荐系统结合、协同过滤增强、可解释推荐等关键词，属于生成式推荐和序列推荐的前沿方向，对工业落地有参考价值。

---

_知识库更新时间：2026-07-12T07:42:44.678831_
