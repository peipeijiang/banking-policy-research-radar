---
title: "DSFNet: Learning Disentangled Scenario Factorization for Multi-Scenario Route Ranking"
paper_id: "https://doi.org/10.1145/3701716.3715219"
source: "www"
published: "2025-01-01T00:00:00"
score: 30.0
tags: ["paper", "recommender-systems", "Data Management and Algorithms", "Data Mining Algorithms and Applications", "Text and Document Classification Technologies"]
---

# DSFNet: Learning Disentangled Scenario Factorization for Multi-Scenario Route Ranking

[查看原文](https://dblp.org/rec/conf/www/0002DXCLLYCG25) · [ArXiv](https://arxiv.org/abs/2404.00243) · [Semantic Scholar](https://www.semanticscholar.org/paper/babab88e662ead916d33c0d7e545a0ec0f1411cf)

## 一句话结论

> 该论文提出DSFNet，通过解耦场景因子解决多场景路线排序中的场景数量爆炸、高纠缠和高容量需求问题，并在新构建的大规模数据集MSDR上验证了有效性，已部署于高德地图。

## 论文信息

- **作者**：J. Yu, Yihai Duan, Longfei Xu, Chao Chen, Shuliang Liu, Kaikui Liu, Fan Yang, Xiangxiang Chu, Ning Guo
- **来源**：WWW
- **发布时间**：2025-01-01
- **相关度评分**：30.0
- **DOI**：[https://doi.org/10.1145/3701716.3715219](https://doi.org/10.1145/3701716.3715219)

<details open>
<summary><strong>中文摘要</strong></summary>

多场景路线排序（Multi-scenario Route Ranking, MSRR）在许多工业地图系统中至关重要。然而，工业界主要采用交互式界面鼓励用户选择预定义场景，这可能阻碍下游排序性能。此外，在学术界，多场景排序研究仅来自其他领域，由于缺乏公开可用的MSRR数据集，目前尚无专门针对路线数据的研究。而且，现有所有多场景工作仍未能同时解决MSRR的三个特定挑战，即场景数量爆炸、高度耦合性和高容量需求。与以往不同，为解决MSRR，我们的核心思想是将路线排序中的复杂场景分解为若干解耦的因子场景模式。据此，我们提出了一种新方法——解耦场景因子网络（Disentangled Scenario Factorization Network, DSFNet），该方法基于高容量多因子场景分支结构灵活组合场景相关参数。随后，提出了一种新的正则化方法以诱导因子场景的解耦。此外，还开发了两种额外的新技术，即场景感知批归一化（scenario-aware batch normalization）和场景感知特征过滤（scenario-aware feature filtering），以提升网络对场景表征的感知能力。同时，为促进学术界对MSRR的研究，我们提出了MSDR——首个大规模公开可用的带标注工业多场景驾驶路线数据集（Multi-Scenario Driving Route dataset）。综合实验结果表明，我们的DSFNet具有优越性，并已成功部署于高德地图（AMap）以服务主要在线交通流量。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Multi-scenario route ranking (MSRR) is crucial in many industrial mapping systems. However, the industrial community mainly adopts interactive interfaces to encourage users to select pre-defined scenarios, which may hinder the downstream ranking performance. In addition, in the academic community, the multi-scenario ranking works only come from other fields, and there are no works specifically focusing on route data due to lacking a publicly available MSRR dataset. Moreover, all the existing multi-scenario works still fail to address the three specific challenges of MSRR simultaneously, i.e. explosion of scenario number, high entanglement, and high-capacity demand. Different from the prior, to address MSRR, our key idea is to factorize the complicated scenario in route ranking into several disentangled factor scenario patterns. Accordingly, we propose a novel method, Disentangled Scenario Factorization Network (DSFNet), which flexibly composes scenario-dependent parameters based on a high-capacity multi-factor-scenario-branch structure. Then, a novel regularization is proposed to induce the disentanglement of factor scenarios. Furthermore, two extra novel techniques, i.e. scenario-aware batch normalization and scenario-aware feature filtering, are developed to improve the network awareness of scenario representation. Additionally, to facilitate MSRR research in the academic community, we propose MSDR, the first large-scale publicly available annotated industrial Multi-Scenario Driving Route dataset. Comprehensive experimental results demonstrate the superiority of our DSFNet, which has been successfully deployed in AMap to serve the major online traffic.

</details>

---

_知识库更新时间：2026-07-13T01:23:50.736331_
