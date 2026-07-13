---
title: "Noise-Separated Bayesian Personalized Ranking for Robust Implicit Recommendation"
paper_id: "https://doi.org/10.5281/zenodo.21304744"
source: "openalex"
published: "2026-07-11T00:00:00"
score: 25.0
tags: ["paper", "recommender-systems", "Recommender Systems and Techniques", "Advanced Bandit Algorithms Research", "Mobile Crowdsensing and Crowdsourcing"]
---

# Noise-Separated Bayesian Personalized Ranking for Robust Implicit Recommendation

[查看原文](https://doi.org/10.5281/zenodo.21304744)

## 一句话结论

> 针对隐式反馈中的点击噪声问题，提出噪声分离的贝叶斯个性化排序（NS-BPR）方法，通过显式建模噪声分布并自适应惩罚噪声样本，提升推荐鲁棒性和准确性。

## 论文信息

- **作者**：Jincheng Zhang
- **来源**：Zenodo (CERN European Organization for Nuclear Research)
- **发布时间**：2026-07-11
- **相关度评分**：25.0
- **DOI**：[https://doi.org/10.5281/zenodo.21304744](https://doi.org/10.5281/zenodo.21304744)

<details open>
<summary><strong>中文摘要</strong></summary>

在大数据时代，隐式反馈（如点击、浏览）因其丰富性和易采集性，已成为构建个性化推荐系统的基石。然而，隐式反馈天然包含大量“点击噪声”（如误触、随机浏览或标题党），这些噪声并不反映用户的真实偏好。传统的贝叶斯个性化排序（Bayesian Personalized Ranking, BPR）算法基于完美观测假设，将所有被点击物品视为正样本、未点击物品视为负样本，因此极易受到点击噪声的干扰并产生过拟合。为解决这一局限，本文提出一种名为噪声分离BPR（Noise-Separated BPR, NS-BPR）的新框架。NS-BPR的核心思想是摒弃简单的“点击即偏好”假设，显式建模点击噪声的分布。我们将可观测的点击行为分解为两种潜在状态：由真实偏好驱动的点击和由随机噪声驱动的点击。通过将这种噪声分离机制融入贝叶斯后验推导，模型能够精确地从后验概率中分离并剥离噪声成分。理论分析与梯度推导表明，NS-BPR在优化过程中通过软梯度截断机制自适应地惩罚噪声样本。该数据驱动框架以完全自监督的方式运行，无需任何人工标注或辅助特征（如停留时长）。NS-BPR有效消除了恶意标题党导致的梯度扭曲，从而保护长尾物品，并显著提升推荐准确性与鲁棒性。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

In the era of big data, implicit feedback (e.g., clicks, views) has become the cornerstone for building personalized recommender systems due to its abundance and ease of collection. However, implicit feedback is inherently contaminated with substantial "clicking noise" (e.g., accidental touches, random browsing, or clickbaits), which does not reflect users' genuine preferences. Traditional Bayesian Personalized Ranking (BPR) algorithms rely on a perfect observation assumption, treating all clicked items as positive samples and unclicked ones as negative samples. Consequently, they exhibit severe vulnerability and overfit to clicking noise. To address this limitation, this paper proposes a novel framework named Noise-Separated BPR (NS-BPR). The core philosophy of NS-BPR is to abandon the simplistic "click-means-preference" assumption and explicitly model the distribution of clicking noise. We decompose the observable clicking behaviors into two latent states: true preference-driven clicks and random noise-driven clicks. By incorporating this noise-separation mechanism into the Bayesian posterior derivation, the model can precisely isolate and strip the noise components from the posterior probability. Theoretical analysis and gradient derivation demonstrate that NS-BPR adaptively penalizes noisy samples via a soft gradient truncation mechanism during the optimization process. This data-driven framework operates in a completely self-supervised manner without requiring any manual annotations or auxiliary features (such as dwell time). NS-BPR effectively eliminates the gradient distortion caused by malicious clickbaits, thereby protecting long-tail items and significantly improving the recommendation accuracy and robustness.

</details>

---

_知识库更新时间：2026-07-12T10:37:28.675687_
