---
title: "MLLMRec：一种结合图优化的多模态推荐偏好推理范式"
paper_id: "https://doi.org/10.1145/3805712.3809749"
source: "openalex"
published: "2026-07-10T00:00:00"
score: 54.0
tags: ["paper", "recommender-systems", "Multimodal Machine Learning Applications", "Recommender Systems and Techniques", "Advanced Graph Neural Networks"]
---

# MLLMRec：一种结合图优化的多模态推荐偏好推理范式

> **英文原标题**：MLLMRec: A Preference Reasoning Paradigm with Graph Refinement for Multimodal Recommendation

[查看原文](https://doi.org/10.1145/3805712.3809749) · [ArXiv](https://arxiv.org/abs/2508.15304)

## 一句话结论

> 提出 MLLMRec 范式，利用多模态大语言模型进行偏好推理和图优化，解决多模态推荐中用户表示初始化和物品图噪声问题，在三个数据集上平均提升21.48%。

## 论文信息

- **作者**：Yuzhuo Dang, Xin Zhang, Zhiqiang Pan, Yuxiao Duan, Wanyu Chen, Fei Cai, Honghui Chen
- **来源**：Proceedings of the 49th International ACM SIGIR Conference on Research and Development in Information Retrieval
- **发布时间**：2026-07-10
- **相关度评分**：54.0
- **DOI**：[https://doi.org/10.1145/3805712.3809749](https://doi.org/10.1145/3805712.3809749)

<details open>
<summary><strong>中文摘要</strong></summary>

多模态推荐将用户历史行为与物品的多模态特征相结合，以捕捉用户显性偏好，相较于传统基于ID的推荐系统展现出更优性能。然而，现有方法在用户与物品的表示学习中仍分别面临两个关键问题：（1）多模态用户表示的初始化要么与历史行为无关，要么受到无关模态噪声的污染；（2）广泛使用的基于KNN的物品-物品图包含低相似度的噪声边，且缺乏受众共现关系。为解决上述问题，我们提出MLLMRec——一种面向多模态推荐的图优化偏好推理范式。具体而言，一方面，首先利用多模态大语言模型（MLLM）将物品图像转化为高质量语义描述，从而弥合视觉与文本模态间的语义鸿沟；随后为每位用户构建行为描述列表，并将其输入MLLM以推理出包含潜在交互意图的纯净用户偏好画像。另一方面，我们开发了阈值控制去噪与拓扑感知增强策略，用于优化次优的物品-物品图，从而提升物品表示学习的准确性。在三个公开数据集上的大量实验表明，MLLMRec实现了最先进的性能，相较于最优基线平均提升21.48%。源代码已提供于https://github.com/Yuzhuo-Dang/MLLMRec。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Multimodal recommendation combines the user historical behaviors with the modal features of items to capture the tangible user preferences, presenting superior performance compared to the conventional ID-based recommender systems. However, existing methods still encounter two key problems in the representation learning of users and items, respectively: (1) the initialization of multimodal user representations is either agnostic to historical behaviors or contaminated by irrelevant modal noise, and (2) the widely used KNN-based item-item graph contains noisy edges with low similarities and lacks audience co-occurrence relationships. To address such issues, we propose MLLMRec, a novel preference reasoning paradigm with graph refinement for multimodal recommendation. Specifically, on the one hand, the item images are first converted into high-quality semantic descriptions using a multimodal large language model (MLLM), thereby bridging the semantic gap between visual and textual modalities. Then, we construct a behavioral description list for each user and feed it into the MLLM to reason about the purified user preference profiles that contain the latent interaction intents. On the other hand, we develop the threshold-controlled denoising and topology-aware enhancement strategies to refine the suboptimal item-item graph, thereby improving the accuracy of item representation learning. Extensive experiments on three publicly available datasets demonstrate that MLLMRec achieves the state-of-the-art performance with an average improvement of 21.48% over the optimal baselines. The source code is provided at https://github.com/Yuzhuo-Dang/MLLMRec.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

多模态推荐通过融合用户历史行为与物品模态特征来捕捉用户偏好，但现有方法存在两个关键问题：用户多模态表示初始化要么忽略历史行为，要么被模态噪声污染；广泛使用的基于KNN的物品-物品图包含低相似度的噪声边，且缺乏受众共现关系。为此，本文提出MLLMRec，一种新颖的偏好推理范式。一方面，利用多模态大语言模型（MLLM）将物品图像转换为高质量语义描述，弥合视觉与文本模态间的语义鸿沟；然后为用户构建行为描述列表，输入MLLM推理出包含潜在交互意图的纯净用户偏好画像。另一方面，设计阈值控制去噪和拓扑感知增强策略来优化次优的物品-物品图，提升物品表示学习精度。在三个公开数据集上的实验表明，MLLMRec平均比最优基线提升21.48%。

### 主要创新

- 利用MLLM推理用户偏好画像，提取潜在交互意图并过滤模态噪声，初始用户表示无需依赖用户-物品图卷积。
- 提出阈值控制去噪策略，结合top-K选择和相似度阈值，剔除低相似度的假阳性边。
- 提出拓扑感知增强策略，通过Jaccard系数计算物品间的受众共现关系，恢复缺失的协同信号边。
- 将语义亲和图与共现图融合，构建更可靠的物品-物品图，提升图卷积的高阶特征捕获能力。

### 研究方法

首先，使用MLLM（Gemma3-27b）将物品图像转换为语义描述，并与文本元数据拼接形成多模态描述。然后，为每个用户按时间顺序聚合交互物品的多模态描述，构建行为描述列表，输入MLLM推理生成用户偏好画像。同时，利用Sentence-Transformer编码多模态描述得到物品特征，计算余弦相似度，结合阈值α和top-K_s进行去噪；再计算用户交互矩阵的Jaccard系数得到共现分数，经top-K_c筛选后与去噪后的语义图相加融合。在融合图上使用LightGCN进行图卷积，得到高阶物品表示。最后，将用户偏好画像通过同一文本编码器映射，与物品表示经MLP投影后，使用BPR损失优化。

### 关键结果

在Baby、Sports、Clothing三个数据集上，MLLMRec在Recall@20和NDCG@20上均取得最优，平均提升21.48%。消融实验表明，移除用户偏好推理模块（w/o RS）导致性能下降最大；移除视觉或文本模态均导致性能下降。兼容性实验显示，使用不同MLLM（Gemma3系列、Llava、Ministral3、Qwen2.5vl）均保持稳健性能，且Gemma3系列存在规模效应。

### 技术栈

- MLLM: Gemma3-27b (Ollama框架)
- 文本编码器: Sentence-Transformer
- 图卷积网络: LightGCN
- 相似度计算: 余弦相似度
- 共现度量: Jaccard系数
- 优化器: Adam
- 损失函数: Bayesian Personalized Ranking (BPR) loss
- 激活函数: LeakyReLU
- 参数初始化: Xavier方法

### 方法优势

- 创新性地利用MLLM进行用户偏好推理，生成行为感知且鲁棒的初始表示，避免传统随机初始化或噪声聚合的缺陷。
- 提出的图优化策略（阈值去噪+拓扑增强）有效降低了物品-物品图的结构噪声，提升了图卷积质量。
- 在三个真实数据集上取得显著性能提升，平均提升21.48%，且消融实验验证了各模块的有效性。
- 兼容性实验表明方法对不同MLLM具有鲁棒性，且存在规模效应。

### 主要局限

- 输入内容未提供明确的局限性讨论。

### 与当前研究方向的关联

多模态推荐: 论文核心研究多模态推荐，利用视觉和文本模态进行用户偏好建模。；LLM与推荐系统结合: 论文使用MLLM进行语义描述生成和用户偏好推理，属于LLM增强推荐。；图神经网络: 论文使用LightGCN在优化的物品-物品图上进行图卷积。；用户建模: 论文通过MLLM推理生成用户偏好画像，实现用户建模。

## 代码与复现

- [Yuzhuo-Dang/MLLMRec](https://github.com/Yuzhuo-Dang/MLLMRec)：official，置信度 100，Stars 23

---

_知识库更新时间：2026-07-12T10:37:28.676446_
