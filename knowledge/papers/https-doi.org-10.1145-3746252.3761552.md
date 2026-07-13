---
title: "Next-Generation Price Recommendation with LLM-Augmented Graph Transformers"
paper_id: "https://doi.org/10.1145/3746252.3761552"
source: "cikm"
published: "2025-01-01T00:00:00"
score: 34.0
tags: ["paper", "recommender-systems", "Recommender Systems and Techniques", "Sharing Economy and Platforms", "Advanced Graph Neural Networks"]
---

# Next-Generation Price Recommendation with LLM-Augmented Graph Transformers

[查看原文](https://dblp.org/rec/conf/cikm/AbachiBMAN25) · [Semantic Scholar](https://www.semanticscholar.org/paper/76e5963ab705455e042464c3ead43ce65a45f363)

## 一句话结论

> 该论文提出一个结合LLM和Graph Transformer的框架，通过LLM生成元特征并利用图神经网络建模房源关系，以提升动态定价推荐的准确性和可解释性。

## 论文信息

- **作者**：Hadi Mohammadzadeh Abachi, Amin Beheshti, Milad Mosharraf, Pooyan Asgari, Majid Namazi
- **来源**：CIKM
- **发布时间**：2025-01-01
- **相关度评分**：34.0
- **DOI**：[https://doi.org/10.1145/3746252.3761552](https://doi.org/10.1145/3746252.3761552)

<details open>
<summary><strong>中文摘要</strong></summary>

在Airbnb等双边平台上，由于房源异质性、用户行为差异以及情境变量的复杂性，动态定价面临诸多挑战。本文提出了一种鲁棒且可解释的定价框架，利用大语言模型（LLMs）与提示工程（prompt engineering），从非结构化和结构化房源数据中自动生成高层级元特征。这些元特征旨在捕捉传统特征工程流程常忽略的细微语义特征。我们进一步将这些表征集成到基于Transformer的图神经网络（GNN）中，该网络以数据驱动和多种关系构建方式，对房源之间的关联与空间依赖关系进行建模。通过将提示驱动嵌入与图感知上下文学习相结合，我们的框架显著提升了价格推荐准确性，同时通过同质性分析（assortativity analysis）提供了透明度。基于真实世界Airbnb数据集的广泛实验表明，该方法在预测性能、跨邻域未见数据泛化能力以及输出可解释性方面均表现优异。本研究凸显了将大语言模型、结构化图学习与可解释人工智能相统一，以构建下一代动态定价系统的潜力。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Dynamic pricing on two-sided platforms such as Airbnb presents complex challenges due to the heterogeneity of listings, user behaviours, and contextual variables. In this work, we propose a robust and interpretable pricing framework that leverages Large Language Models (LLMs) and prompt engineering to automate the generation of high-level meta-features from unstructured and structured listing data. These meta-features are designed to capture nuanced semantic features that are often overlooked by traditional feature engineering pipelines. We further integrate these representations into a Transformer-based Graph Neural Network (GNN), which models the relational and spatial dependencies between listings in a data-driven and several relation-construction manner. By combining prompt-driven embeddings with graph-aware contextual learning, our framework significantly enhances price recommendation accuracy while offering transparency through assortativity analysis. Extensive experiments on real-world Airbnb datasets demonstrate our approach's performance in both prediction and unseen data across neighbourhoods and output interpretability. This work highlights the potential of unifying LLMs, structured graph learning, and interpretable AI for next-generation dynamic pricing systems.

</details>

---

_知识库更新时间：2026-07-12T10:37:28.677969_
