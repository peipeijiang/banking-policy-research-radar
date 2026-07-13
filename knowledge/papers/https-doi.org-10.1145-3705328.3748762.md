---
title: "Bayesian Perspectives on Offline Evaluation for Recommender Systems"
paper_id: "https://doi.org/10.1145/3705328.3748762"
source: "recsys"
published: "2025-01-01T00:00:00"
score: 20.0
tags: ["paper", "recommender-systems", "Advanced Bandit Algorithms Research", "Recommender Systems and Techniques", "Consumer Market Behavior and Pricing"]
---

# Bayesian Perspectives on Offline Evaluation for Recommender Systems

[查看原文](https://dblp.org/rec/conf/recsys/Benigni25)

## 一句话结论

> 该论文提出利用贝叶斯统计方法改进推荐系统的离线评估，通过建模不确定性提高评估的可靠性和鲁棒性。

## 论文信息

- **作者**：Michael Benigni
- **来源**：RecSys
- **发布时间**：2025-01-01
- **相关度评分**：20.0
- **DOI**：[https://doi.org/10.1145/3705328.3748762](https://doi.org/10.1145/3705328.3748762)

<details open>
<summary><strong>中文摘要</strong></summary>

离线评估是推荐系统部署与优化中的基础环节。近年来，情境赌博机框架已成为离线评估与反事实评估的重要方法，促使基于逆倾向得分（IPS）、直接方法（DM）及双重稳健（DR）技术的估计器日益受到关注。然而，现有方法几乎全部依赖频率学派统计，限制了其捕捉模型不确定性并将其反映在评估结果中的能力。本研究探索了贝叶斯统计在推荐任务离线策略评估中的新研究方向，其动机源于对更稳健应对分布偏移、数据稀疏及模型误设的可靠估计器的需求。本文识别出三个尚未充分探索的研究方向：（i）利用贝叶斯奖励模型的后验不确定性设计自适应混合估计器；（ii）通过联合概率框架显式建模离线策略评估问题的所有组成部分（情境、动作与奖励）；（iii）通过后验推断量化策略价值估计的认知不确定性。通过借助贝叶斯框架，旨在提升离线评估协议的可靠性、可解释性与安全性，为推荐系统研究中最持久的挑战之一提供新视角。这一视角在数据稀缺或高风险场景中尤为重要，因为理解不确定性对于可信决策至关重要。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Offline evaluation is a fundamental component in the deployment and development of better recommender systems. In recent years, the contextual bandit framework has emerged as a valuable approach for offline and counterfactual evaluation, leading to the increasing interest in estimators based on inverse propensity scoring (IPS), direct methods (DM), and doubly robust (DR) techniques. However, nearly all existing methods rely on frequentist statistics, limiting their ability to capture model uncertainty and reflecting it in evaluation outcomes.This work explores the novel research direction of Bayesian statistics for Off-Policy Evaluation in recommendation tasks, motivated by the need for reliable estimators that are more robust to distribution shift, data sparsity, and model misspecification. Three underexplored research directions are identified in this work: (i) using posterior uncertainty from Bayesian reward models to design adaptive hybrid estimators, (ii) explicitly modeling all components of the OPE problem (contexts, actions, and rewards) using a joint probabilistic framework, and (iii) quantifying epistemic uncertainty over policy value estimates via posterior inference.By leveraging the Bayesian framework, the aim is to improve the reliability, interpretability, and safety of offline evaluation protocols, offering a new perspective on one of the most persistent challenges in recommender systems research. This perspective is especially relevant in data-scarce or high-stakes settings, where understanding uncertainty is essential for trustworthy decision-making.

</details>

---

_知识库更新时间：2026-07-12T11:20:57.447040_
