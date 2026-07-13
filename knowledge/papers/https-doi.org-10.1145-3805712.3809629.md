---
title: "AsarRec：面向鲁棒自监督序列推荐的自适应序列增强"
paper_id: "https://doi.org/10.1145/3805712.3809629"
source: "openalex"
published: "2026-07-10T00:00:00"
score: 38.0
tags: ["paper", "recommender-systems", "Recommender Systems and Techniques", "Advanced Bandit Algorithms Research", "Advanced Technologies in Various Fields"]
---

# AsarRec：面向鲁棒自监督序列推荐的自适应序列增强

> **英文原标题**：AsarRec: Adaptive Sequential Augmentation for Robust Self-supervised Sequential Recommendation

[查看原文](https://doi.org/10.1145/3805712.3809629) · [ArXiv](https://arxiv.org/abs/2512.14047)

## 一句话结论

> 提出自适应序列增强框架AsarRec，通过可微的Semi-Sinkhorn算法学习最优数据增强策略，提升序列推荐在噪声环境下的鲁棒性。

## 论文信息

- **作者**：Kaike Zhang, Qi Cao, Fei Sun, Xinran Liu, Huawei Shen, Xueqi Cheng
- **来源**：Proceedings of the 49th International ACM SIGIR Conference on Research and Development in Information Retrieval
- **发布时间**：2026-07-10
- **相关度评分**：38.0
- **DOI**：[https://doi.org/10.1145/3805712.3809629](https://doi.org/10.1145/3805712.3809629)

<details open>
<summary><strong>中文摘要</strong></summary>

现实世界中的用户行为常因人为错误、不确定性及行为模糊性等因素而带有噪声，这可能导致推荐性能下降。为解决该问题，近期研究广泛采用自监督学习（SSL），尤其是对比学习，通过生成用户交互序列的扰动视图并最大化其互信息来提升模型鲁棒性。然而，这些方法高度依赖预定义的静态增强策略（即增强类型一旦选定便固定不变）来构建增强视图，由此引发两个关键挑战：（1）最优增强类型在不同场景下可能存在显著差异；（2）不恰当的增强甚至可能降低推荐性能，从而限制SSL的有效性。为克服上述局限，我们提出一种自适应增强框架。首先，通过结构化变换矩阵将现有基础增强操作统一为统一公式。基于该公式，我们提出AsarRec——面向鲁棒序列推荐的自适应序列增强方法。为实现离散且强约束增强的稳定端到端优化，AsarRec通过将用户序列编码为概率转移矩阵，并利用可微分的半Sinkhorn算法将其投影为硬半双随机矩阵，从而学习生成变换矩阵。为确保所学增强有利于下游性能，我们联合优化三个目标：多样性（鼓励生成差异化视图）、语义不变性（保持视图间的语义一致性）以及信息性（识别对推荐最有益的增强）。在四种不同噪声水平的基准数据集上进行的广泛实验验证了AsarRec的有效性，证明了其卓越的鲁棒性与持续的性能提升。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Real-world user behaviors are often noisy due to factors such as human errors, uncertainty, and behavioral ambiguity, which can lead to degraded recommendation performance. To address this issue, recent approaches widely adopt self-supervised learning (SSL), particularly contrastive learning, by generating perturbed views of user interaction sequences and maximizing their mutual information to improve model robustness. However, these methods heavily rely on their pre-defined static augmentation strategies~(where the augmentation type remains fixed once chosen) to construct augmented views, leading to two critical challenges: (1) the optimal augmentation type can vary significantly across different scenarios; (2) inappropriate augmentations may even degrade recommendation performance, limiting the effectiveness of SSL. To overcome these limitations, we propose an adaptive augmentation framework. We first unify existing basic augmentation operations into a unified formulation via structured transformation matrices. Building on this formulation, we introduce AsarRec, an Adaptive Sequential Augmentation for Robust Sequential Recommendation. To enable stable end-to-end optimization of discrete and strongly constrained augmentations, AsarRec learns to generate transformation matrices by encoding user sequences into probabilistic transition matrices and projecting them into hard semi-doubly stochastic matrices via a differentiable Semi-Sinkhorn algorithm. To ensure that the learned augmentations benefit downstream performance, we jointly optimize three objectives: diversity (encouraging distinct views), semantic invariance (preserving semantic consistency among views), and informativeness (identifying augmentations most beneficial to recommendation). Extensive experiments on four benchmarks under varying noise levels validate the effectiveness of AsarRec, demonstrating its superior robustness and consistent improvements.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

本文针对现有自监督序列推荐方法中静态增强策略（如掩码、重排等）无法适应不同场景、甚至可能损害性能的问题，提出自适应增强框架AsarRec。首先将五种基本增强操作统一为结构化变换矩阵（硬半双随机矩阵），然后通过可微分的半Sinkhorn算法将用户序列编码为概率转移矩阵并投影为离散矩阵，实现端到端优化。为保障增强效果，联合优化三个目标：多样性（鼓励不同视图）、语义不变性（保持序列语义）和信息性（构造有挑战性的视图）。在四个基准数据集上，AsarRec在干净和不同噪声水平下均显著优于现有方法，验证了其鲁棒性和有效性。

### 主要创新

- 将五种基本序列增强操作统一为硬半双随机矩阵变换，实现可学习的自适应增强框架。
- 提出可微分的半Sinkhorn算法，将连续概率矩阵投影为离散变换矩阵，支持端到端优化。
- 联合优化多样性、语义不变性和信息性三个目标，确保增强既合理又有益于推荐。
- 在训练阶段自适应生成增强，推理时无额外开销，易于集成到现有推荐系统。

### 研究方法

首先，将Crop、Mask、Reorder、Insert、Substitute五种增强操作统一表示为硬半双随机矩阵与序列的乘积。然后，通过编码模块（线性变换+自注意力）生成概率转移矩阵，再利用可微分的半Sinkhorn算法迭代行/列归一化并逐步硬化，得到离散变换矩阵。最后，联合优化InfoNCE损失（信息性）、基于L2范数的多样性损失和基于序列感知NDCG的语义不变性损失，训练编码模块。

### 关键结果

在Games、Arts、MIND、ML-20M四个数据集上，AsarRec在HR@10/20和NDCG@10/20上均显著优于所有基线（如CL4Rec、CoSeRec、S3Rec等），相对提升最高达13.49%。；在0.1至0.5噪声比例下，AsarRec性能下降最慢，始终优于其他方法，表现出强鲁棒性。；在GRU4rec和FMLPrec两种骨干模型上，AsarRec同样取得一致提升，验证了泛化性。；变换矩阵可视化显示，AsarRec倾向于在序列首尾进行强扰动，避免长距离重排，且噪声环境下扰动更集中。

### 技术栈

- 硬半双随机矩阵
- 可微分半Sinkhorn算法
- 自注意力机制
- InfoNCE损失
- 序列感知NDCG
- L2范数

### 方法优势

- 创新性地将离散增强操作统一为可学习的矩阵变换，解决了静态增强的适应性问题。
- 提出的三个优化目标从不同角度保障增强质量，设计合理。
- 实验充分，涵盖多个数据集、噪声水平、骨干模型和基线，结果全面且显著。
- 推理时无额外开销，实用性强。

### 主要局限

- 输入内容未提供消融实验的具体数值，仅提及多样性约束对训练稳定性的重要性。
- 输入内容未讨论超参数（如λ_div、λ_NDCG）的敏感性分析。
- 输入内容未提及在更复杂增强（如基于知识图谱）上的对比。
- 方法依赖于可微分Sinkhorn的迭代，可能增加训练时间（但输入内容未提供具体复杂度对比）。

### 与当前研究方向的关联

序列推荐：论文聚焦于序列推荐中的自监督增强方法。；鲁棒性：核心目标是提升推荐系统对噪声的鲁棒性。；自监督学习：采用对比学习框架，自适应生成增强视图。；自适应增强：提出动态调整增强策略的方法。

---

_知识库更新时间：2026-07-12T10:37:28.675851_
