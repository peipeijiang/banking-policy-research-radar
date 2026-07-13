---
title: "TransAct V2：Pinterest推荐中的终身用户行为序列建模"
paper_id: "https://doi.org/10.1145/3746252.3761433"
source: "cikm"
published: "2025-01-01T00:00:00"
score: 60.0
tags: ["paper", "recommender-systems", "Recommender Systems and Techniques", "Mobile Crowdsensing and Crowdsourcing", "Personal Information Management and User Behavior"]
---

# TransAct V2：Pinterest推荐中的终身用户行为序列建模

> **英文原标题**：TransAct V2: Lifelong User Action Sequence Modeling on Pinterest Recommendation

[查看原文](https://dblp.org/rec/conf/cikm/0007JRLLPB0E25) · [ArXiv](https://arxiv.org/abs/2506.02267) · [Semantic Scholar](https://www.semanticscholar.org/paper/b8a521315046b1bab0e215d06455429c67d70fd9)

## 一句话结论

> 该论文提出TransAct V2，通过利用超长用户序列、可扩展的低延迟部署和下一动作损失函数，显著提升了Pinterest Homefeed排序系统的CTR预测和推荐多样性。

## 论文信息

- **作者**：X.-G. Xia, Saurabh Vishwas Joshi, Kousik Rajesh, Kangnan Li, Yangyi Lu, Nikil Pancha, Dhruvil Badani, Jiajing Xu, Pong Eksombatchai
- **来源**：CIKM
- **发布时间**：2025-01-01
- **相关度评分**：60.0
- **DOI**：[https://doi.org/10.1145/3746252.3761433](https://doi.org/10.1145/3746252.3761433)

<details open>
<summary><strong>中文摘要</strong></summary>

对用户行为序列的建模已成为工业推荐系统研究的热点方向，尤其在点击率（Click-Through Rate, CTR）预测任务中。然而，工业级CTR模型通常依赖短用户序列，限制了其捕捉长期行为的能力。这类模型也鲜少解决高效服务大规模序列模型所涉及的基础设施挑战。此外，在逐点排序框架下，这些模型通常缺乏集成的行为预测任务，从而削弱了其预测能力。我们提出TransAct V2——Pinterest首页排序系统的生产级模型，其包含三项关键创新：（1）利用超长用户序列提升CTR预测效果；（2）采用可扩展、低延迟的部署方案，以应对扩展用户行为序列带来的计算需求；（3）集成下一行为损失函数（Next Action Loss），增强用户行为预测能力。为克服延迟与存储限制，我们借助高效的数据处理策略与模型服务优化，实现了无缝的工业级部署。消融实验进一步验证了本方法的有效性。此外，大量离线与在线A/B实验证实，该方法在关键指标（包括参与度与推荐多样性）上取得了显著提升，展示了TransAct V2的实际应用价值。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Modeling user action sequences has become a popular focus in industrial recommendation system research, particularly for Click-Through Rate (CTR) prediction tasks. However, industry-scale CTR models often rely on short user sequences, limiting their ability to capture long-term behavior. They also rarely address the infrastructure challenges involved in efficiently serving large-scale sequential models. Additionally, these models typically lack an integrated action-prediction task within a point-wise ranking framework, reducing their predictive power. We introduce TransAct V2, a production model for Pinterest's Homefeed ranking system, featuring three key innovations: (1) leveraging very long user sequences to improve CTR predictions, (2) employing scalable, low-latency deployment solutions tailored to handle the computational demands of extended user action sequences, and (3) integrating a Next Action Loss function for enhanced user action forecasting. To overcome latency and storage constraints, we leverage efficient data-processing strategies and model-serving optimizations, enabling seamless industrial-scale deployment. Our approach's effectiveness is further demonstrated through ablation studies. Furthermore, extensive offline and online A/B experiments confirm major gains in key metrics, including engagement volume and recommendation diversity, showcasing TransAct V2's real-world impact.

</details>

## 深度解读

> 分析依据：**AI 深度分析**

### 核心结论

本文介绍了TransAct V2，一个用于Pinterest首页推荐的生产级模型。该模型通过三个关键创新改进了点击率（CTR）预测：利用超长用户序列、集成下一动作损失函数以及采用可扩展的低延迟部署方案。TransAct V2结合实时和终身用户序列，通过下一动作预测任务增强对用户偏好的理解，并提升推荐多样性。系统设计高效处理长达10^4的终身序列，同时保持低延迟、低存储和低网络成本。离线与在线A/B实验表明，该模型在用户参与度和推荐多样性等关键指标上取得了显著提升，目前已服务于Pinterest超过5亿用户。

### 主要创新

- 利用终身用户序列（长达2年）改进CTR预测，突破传统短序列限制。
- 集成下一动作损失函数，增强模型对用户行为的预测能力。
- 采用可扩展的低延迟部署方案，包括量化、近邻搜索和特征缓存，支持工业级实时服务。
- 在点式排序框架中整合动作预测任务，提升预测准确性。

### 研究方法

论文采用基于Transformer的序列建模方法。首先，使用候选物品作为锚点，对终身序列、实时序列和曝光序列进行近邻搜索，并保留最近动作。然后，将子序列拼接后输入Transformer编码器，结合位置编码和特征嵌入（动作类型、表面、PinSage嵌入）。模型采用多任务学习架构，主任务为CTR预测（加权交叉熵损失），辅助任务为下一动作预测（对比损失）。训练时使用负采样和样本加权。部署时通过离线特征缓存、量化（fp16→int8）和近邻搜索优化延迟。

### 关键结果

在线A/B实验显示，用户参与度指标（如点击率、保存率）显著提升。；推荐多样性指标（如类别覆盖率）得到改善。；离线消融实验验证了终身序列、下一动作损失和部署优化的各自贡献。；模型成功部署于Pinterest首页推荐，服务超过5亿用户。

### 技术栈

- Transformer
- 近邻搜索（Nearest Neighbor Search）
- PinSage嵌入
- 量化（int8量化）
- 多任务学习（MTL）
- 加权交叉熵损失
- 对比损失（下一动作损失）
- 特征缓存

### 方法优势

- 创新性地结合终身和实时序列，平衡短期与长期兴趣。
- 引入下一动作预测任务，增强CTR模型的预测能力。
- 工业级部署方案兼顾低延迟和低成本，具有实际应用价值。
- 在Pinterest大规模真实场景中验证有效性，结果可靠。

### 主要局限

- 终身序列长度受限于90百分位，可能忽略极长尾用户行为。
- 近邻搜索依赖PinSage嵌入质量，可能对冷启动物品不友好。
- 模型复杂度较高，训练和部署资源需求大。
- 未与生成式推荐模型（如HSTU）进行直接比较。

### 与当前研究方向的关联

序列推荐：核心研究内容，建模用户行为序列。；CTR预测：主要任务，通过序列建模提升点击率预测。；用户建模：通过终身序列和实时序列建模用户兴趣。；工业落地：论文详细描述了部署优化和实际效果。；排序与重排：应用于推荐系统的排序阶段。

---

_知识库更新时间：2026-07-12T07:42:44.681652_
