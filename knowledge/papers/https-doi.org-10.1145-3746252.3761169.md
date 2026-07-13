---
title: "通过多模态嵌入和语义ID增强大语言模型用于序列推荐"
paper_id: "https://doi.org/10.1145/3746252.3761169"
source: "cikm"
published: "2025-01-01T00:00:00"
score: 70.0
tags: ["paper", "recommender-systems", "Recommender Systems and Techniques", "Machine Learning in Healthcare", "Advanced Graph Neural Networks"]
---

# 通过多模态嵌入和语义ID增强大语言模型用于序列推荐

> **英文原标题**：Empowering Large Language Model for Sequential Recommendation via Multimodal Embeddings and Semantic IDs

[查看原文](https://dblp.org/rec/conf/cikm/0006P0000LJ025) · [ArXiv](https://arxiv.org/abs/2509.02017) · [Semantic Scholar](https://www.semanticscholar.org/paper/58f675de28bfc716ede80dd16e0a19853bf67439)

## 一句话结论

> 该论文提出MME-SID框架，通过多模态嵌入和语义ID解决LLM在序列推荐中的嵌入坍缩和灾难性遗忘问题，实验验证了其优越性能。

## 论文信息

- **作者**：Yuhao Wang, Junwei Pan, Xinhang Li, Maolin Wang, Yuan Wang, Yue Liu, Dapeng Liu, Jie Jiang, Xiangyu Zhao
- **来源**：CIKM
- **发布时间**：2025-01-01
- **相关度评分**：70.0
- **DOI**：[https://doi.org/10.1145/3746252.3761169](https://doi.org/10.1145/3746252.3761169)

<details open>
<summary><strong>中文摘要</strong></summary>

序列推荐（Sequential Recommendation, SR）旨在基于用户的历史交互行为捕捉其动态兴趣与序列模式。近年来，大语言模型（Large Language Models, LLMs）的强大能力推动了其在SR领域的应用。然而，我们识别出现有基于LLM的SR方法中存在的两个关键挑战：1）在融合预训练协同嵌入时出现嵌入坍缩（embedding collapse）；2）使用语义ID时量化嵌入的灾难性遗忘（catastrophic forgetting）。这些问题削弱了模型的可扩展性，并导致推荐性能欠优。因此，基于Llama3-8B-instruct等LLM，我们提出了一种名为MME-SID的新型SR框架，该框架通过整合多模态嵌入与量化嵌入来缓解嵌入坍缩。此外，我们提出了一种多模态残差量化变分自编码器（Multimodal Residual Quantized Variational Autoencoder, MM-RQ-VAE），采用最大均值差异作为重构损失，并利用对比学习进行对齐，从而分别有效保留模态内距离信息并捕获模态间相关性。为进一步缓解灾难性遗忘，我们使用训练好的多模态码本嵌入对模型进行初始化。最后，我们以多模态频率感知融合方式，通过LoRA对LLM进行高效微调。在三个公开数据集上的大量实验验证了MME-SID的优越性能，这得益于其缓解嵌入坍缩与灾难性遗忘的能力。实现代码与数据集已公开以供复现：https://github.com/Applied-Machine-Learning-Lab/MME-SID。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Sequential recommendation (SR) aims to capture users' dynamic interests and sequential patterns based on their historical interactions. Recently, the powerful capabilities of large language models (LLMs) have driven their adoption in SR. However, we identify two critical challenges in existing LLM-based SR methods: 1) embedding collapse when incorporating pre-trained collaborative embeddings and 2) catastrophic forgetting of quantized embeddings when utilizing semantic IDs. These issues dampen the model scalability and lead to suboptimal recommendation performance. Therefore, based on LLMs like Llama3-8B-instruct, we introduce a novel SR framework named MME-SID, which integrates multimodal embeddings and quantized embeddings to mitigate embedding collapse. Additionally, we propose a Multimodal Residual Quantized Variational Autoencoder (MM-RQ-VAE) with maximum mean discrepancy as the reconstruction loss and contrastive learning for alignment, which effectively preserve intra-modal distance information and capture inter-modal correlations, respectively. To further alleviate catastrophic forgetting, we initialize the model with the trained multimodal code embeddings. Finally, we fine-tune the LLM efficiently using LoRA in a multimodal frequency-aware fusion manner. Extensive experiments on three public datasets validate the superior performance of MME-SID thanks to its capability to mitigate embedding collapse and catastrophic forgetting. The implementation code and datasets are publicly available for reproduction: https://github.com/Applied-Machine-Learning-Lab/MME-SID.

</details>

## 深度解读

> 分析依据：**AI 深度分析**

### 核心结论

本文针对现有基于大语言模型（LLM）的序列推荐方法中存在的两个关键挑战：嵌入坍塌（embedding collapse）和灾难性遗忘（catastrophic forgetting），提出了一种名为MME-SID的新框架。该框架通过引入多模态嵌入和量化嵌入来缓解嵌入坍塌，并设计了一种多模态残差量化变分自编码器（MM-RQ-VAE），使用最大均值差异作为重构损失并结合对比学习，以有效保留模态内距离信息和捕获模态间相关性。为了进一步缓解灾难性遗忘，模型使用训练好的多模态码嵌入进行初始化，并通过LoRA以多模态频率感知融合方式进行高效微调。在三个公开数据集上的实验表明，MME-SID在缓解嵌入坍塌和灾难性遗忘方面表现优越，显著提升了推荐性能。

### 主要创新

- 首次系统性地识别并解决了LLM4SR中的嵌入坍塌和灾难性遗忘问题。
- 提出MM-RQ-VAE，利用最大均值差异作为重构损失，更好地保留距离信息，缓解遗忘。
- 引入对比学习目标以捕获多模态间的相关性。
- 提出多模态频率感知融合的LoRA微调方法，高效利用多模态信息。
- 通过初始化多模态语义ID嵌入来缓解灾难性遗忘。

### 研究方法

本文首先通过理论分析和实验验证了嵌入坍塌和灾难性遗忘的存在。然后，设计MM-RQ-VAE模型，将多模态嵌入（协同、文本、视觉）编码为语义ID，使用最大均值差异损失和对比学习进行训练。接着，将训练好的码嵌入初始化LLM中的语义ID嵌入，并采用LoRA进行多模态频率感知融合微调。最后，在Amazon三个数据集上进行序列推荐任务评估。

### 关键结果

MME-SID在三个Amazon数据集上均取得了优于基线方法的推荐性能。；嵌入坍塌分析显示，MME-SID的嵌入矩阵有效秩显著高于基线，缓解了坍塌。；灾难性遗忘分析表明，MME-SID保留了更多的距离信息（Kendall's tau更高）。；消融实验验证了多模态融合、MM-RQ-VAE损失设计和初始化策略的有效性。

### 技术栈

- 大语言模型：Llama3-8B-instruct
- 量化模型：残差量化变分自编码器（RQ-VAE）
- 损失函数：最大均值差异（MMD）、对比学习损失、均方误差
- 微调方法：LoRA（低秩适应）
- 评估指标：Kendall's tau、推荐准确率指标（如NDCG、Recall）

### 方法优势

- 问题定义清晰，首次系统性地解决LLM4SR中的嵌入坍塌和灾难性遗忘。
- 方法创新性强，结合多模态信息和量化技术，理论分析扎实。
- 实验充分，包括主实验、消融、可视化分析，验证了方法的有效性。
- 代码和数据集公开，可复现。

### 主要局限

- 方法复杂度较高，训练和推理成本可能较大。
- 仅使用了三个Amazon数据集，泛化性需在更多场景验证。
- 对多模态数据的质量依赖较强，噪声数据可能影响性能。
- 未讨论模型在冷启动场景下的表现。

### 与当前研究方向的关联

论文紧密围绕序列推荐、多模态推荐、大语言模型与推荐系统结合、语义ID等关键词，针对LLM4SR中的核心问题提出解决方案，与推荐系统前沿方向高度相关。

## 代码与复现

- [Applied-Machine-Learning-Lab/MME-SID](https://github.com/Applied-Machine-Learning-Lab/MME-SID)：official，置信度 100，Stars 30

---

_知识库更新时间：2026-07-12T07:42:44.679180_
