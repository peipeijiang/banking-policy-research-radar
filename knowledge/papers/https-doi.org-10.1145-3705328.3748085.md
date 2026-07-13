---
title: "面向基于大语言模型推荐的异构用户建模"
paper_id: "https://doi.org/10.1145/3705328.3748085"
source: "recsys"
published: "2025-01-01T00:00:00"
score: 50.0
tags: ["paper", "recommender-systems", "Recommender Systems and Techniques", "Topic Modeling", "Web Data Mining and Analysis"]
---

# 面向基于大语言模型推荐的异构用户建模

> **英文原标题**：Heterogeneous User Modeling for LLM-based Recommendation

[查看原文](https://dblp.org/rec/conf/recsys/Bao0LZSFC25) · [ArXiv](https://arxiv.org/abs/2507.04626)

## 一句话结论

> 该论文提出异构用户建模方法（HUM），通过压缩增强器和鲁棒增强器解决LLM推荐中跨域异构行为建模的泛化性差、噪声压缩和领域跷跷板问题，实验验证了其有效性和鲁棒性。

## 论文信息

- **作者**：Honghui Bao, Wenjie Wang, Xinyu Lin, Fengbin Zhu, Teng Sun, Fuli Feng, Tat‐Seng Chua
- **来源**：RecSys
- **发布时间**：2025-01-01
- **相关度评分**：50.0
- **DOI**：[https://doi.org/10.1145/3705328.3748085](https://doi.org/10.1145/3705328.3748085)

<details open>
<summary><strong>中文摘要</strong></summary>

利用大型语言模型（LLMs）进行推荐已在多个领域展现出显著成效，彰显了其在开放域推荐中的潜力。推进开放域推荐的关键挑战在于如何从用户跨多个领域的异构行为中有效建模用户偏好。现有方法（包括基于ID的建模和基于语义的建模）存在泛化能力差、无法有效压缩噪声交互以及领域跷跷板现象等问题。为解决这些挑战，我们提出了一种异构用户建模（HUM）方法，该方法为基于LLM的推荐引入了压缩增强器与鲁棒性增强器。压缩增强器通过定制化提示将异构行为压缩为定制化令牌，同时利用掩码机制增强跨域知识提取与理解；鲁棒性增强器则引入领域重要性分数，通过引导领域优化来缓解领域跷跷板现象。在异构数据集上的大量实验表明，HUM通过实现高效性与鲁棒性的双重目标，有效建模了用户异构性，从而在开放域推荐中取得了优越性能。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Leveraging Large Language Models (LLMs) for recommendation has demonstrated notable success in various domains, showcasing their potential for open-domain recommendation. A key challenge to advancing open-domain recommendation lies in effectively modeling user preferences from users' heterogeneous behaviors across multiple domains. Existing approaches, including ID-based and semantic-based modeling, struggle with poor generalization, an inability to compress noisy interactions effectively, and the domain seesaw phenomenon. To address these challenges, we propose a Heterogeneous User Modeling (HUM) method, which incorporates a compression enhancer and a robustness enhancer for LLM-based recommendation. The compression enhancer uses a customized prompt to compress heterogeneous behaviors into a tailored token, while a masking mechanism enhances cross-domain knowledge extraction and understanding. The robustness enhancer introduces a domain importance score to mitigate the domain seesaw phenomenon by guiding domain optimization. Extensive experiments on heterogeneous datasets validate that HUM effectively models user heterogeneity by achieving both high efficacy and robustness, leading to superior performance in open-domain recommendation.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

本文针对开放域推荐中用户异构行为建模的挑战，提出异构用户建模方法HUM。现有方法（如ID建模和语义建模）存在泛化差、无法有效压缩噪声交互以及领域跷跷板现象等问题。HUM包含压缩增强器和鲁棒性增强器：压缩增强器通过定制提示将异构行为压缩为专用用户令牌，并利用掩码机制增强跨域知识提取；鲁棒性增强器引入领域重要性分数以平衡各领域优化，缓解领域跷跷板现象。在异构数据集上的实验表明，HUM在有效性和鲁棒性上均优于现有方法，在开放域推荐中表现优异。

### 主要创新

- 提出压缩增强器，利用定制提示和专用用户令牌将异构用户行为压缩为紧凑表示，并采用掩码机制促进跨域知识提取。
- 提出鲁棒性增强器，通过领域重要性分数动态调整各领域优化权重，缓解领域跷跷板现象。
- 在LLM推荐框架中同时实现强压缩能力和强鲁棒性，显著提升异构用户建模效果。

### 研究方法

HUM基于Qwen2.5-1.5b LLM，采用LoRA参数高效微调。压缩增强器：设计压缩提示和[USER]令牌，将用户历史交互序列输入LLM，提取[USER]令牌的隐藏向量作为用户表示；训练时随机掩码部分目标域物品以增强跨域学习。鲁棒性增强器：基于各领域平均训练损失计算领域重要性分数，并通过KL散度正则化进行平滑更新，最终加权各领域损失进行优化。推理时去掩码，计算用户与物品表示的内积进行推荐。

### 关键结果

HUM在六个域（Books、Office、Scientific、CDs、Auto、Tools）上全面优于ID建模和语义建模基线，Recall@10和NDCG@10均最高。；消融实验表明压缩提示、用户令牌和掩码机制均对性能有贡献。；鲁棒性增强器有效缓解了领域跷跷板现象，使各域性能更均衡。；HUM在噪声抵抗实验中，即使100%用户含噪声仍优于LLM-Rec-Qwen。；在四个未见域（Instruments、Games、Arts、Sports）上HUM泛化性能最佳。；随着域数量增加（2域→6域→10域），HUM性能优势扩大。

### 技术栈

- Qwen2.5-1.5b
- LoRA
- AdamW优化器
- 对比学习（InfoNCE损失）
- KL散度
- KKT条件

### 方法优势

- 针对异构用户建模的两个核心问题（压缩噪声和领域平衡）提出了明确且有效的解决方案。
- 实验设计全面，包括主实验、消融、噪声鲁棒性、泛化性和可扩展性分析。
- 方法基于LLM，利用其世界知识和指令跟随能力，具有较好的可迁移性。
- 代码和数据集已开源，可复现。

### 主要局限

- 输入内容未提供计算效率或推理延迟的分析。
- 仅基于Amazon数据集，未在更多平台验证。
- 领域重要性分数依赖训练损失，可能受损失函数设计影响。
- 未讨论用户令牌长度或压缩比的具体影响。

### 与当前研究方向的关联

LLM与推荐系统结合：核心方法基于LLM（Qwen）进行用户建模。；用户建模：直接针对异构用户行为建模，提出压缩和鲁棒增强。；序列推荐：用户历史按时间顺序处理，采用序列输入。；生成式推荐：虽未直接生成，但利用LLM的压缩能力生成用户表示。；工业落地：LoRA微调、开源代码，具备一定实用性。

## 代码与复现

- [HonghuiBao2000/HUM](https://github.com/HonghuiBao2000/HUM)：official，置信度 100，Stars 9
- [TinyMirable/hum_research](https://github.com/TinyMirable/hum_research)：possible，置信度 30，Stars 0

---

_知识库更新时间：2026-07-12T11:20:57.446869_
