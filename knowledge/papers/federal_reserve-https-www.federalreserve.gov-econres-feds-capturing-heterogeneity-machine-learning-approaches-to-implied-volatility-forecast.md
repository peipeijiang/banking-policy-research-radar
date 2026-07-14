---
title: "FEDS Paper: Capturing Heterogeneity: Machine Learning Approaches to Implied Volatility Forecasting"
paper_id: "federal_reserve:https://www.federalreserve.gov/econres/feds/capturing-heterogeneity-machine-learning-approaches-to-implied-volatility-forecasting.htm"
source: "federal_reserve"
published: "2026-07-07T13:15:00"
score: 0.0
tags: ["paper", "banking-fiscal-monetary-policy"]
---

# FEDS Paper: Capturing Heterogeneity: Machine Learning Approaches to Implied Volatility Forecasting

[查看原文](https://www.federalreserve.gov/econres/feds/capturing-heterogeneity-machine-learning-approaches-to-implied-volatility-forecasting.htm)

## 一句话结论

> 该论文提出基于回归树的机器学习框架，通过分割期权曲面提高隐含波动率预测精度，在S&P 500期权数据上显著降低预测误差。

## 论文信息

- **作者**：-
- **来源**：Federal Reserve FEDS and IFDP
- **发布时间**：2026-07-07
- **相关度评分**：0.0
- **DOI**：-

## 相关性评分

- **商业银行**：0.0/10（最高匹配）
- **货币政策**：0.0/10
- **财政政策**：0.0/10
- **评分依据**：论文摘要

> 最高匹配领域：商业银行 0.0/10。论文研究隐含波动率预测，使用机器学习方法对期权曲面进行分割，属于金融计量和衍生品定价领域。不涉及商业银行、货币政策或财政政策的核心问题。三个领域均无实质关联。

<details open>
<summary><strong>中文摘要</strong></summary>

Hyung Joo Kim 与 Dong Hwan Oh 指出，尽管期权曲面上的波动率动态存在已记录在案的异质性，但标准隐含波动率预测模型在整个曲面上均采用同质参数。我们引入一种机器学习框架，利用回归树沿货币性（moneyness）和期限（maturity）两个维度对曲面进行划分，识别出不同预测模型表现最优的数据驱动区域。通过扩展 Dufays、Jacobs 与 Rombouts（2025）提出的曲面异质自回归（Surface Heterogeneous Autoregressive, SHAR）框架，我们开发了基于树的 SHAR 规范，在保留可解释结构的同时，允许模型参数随曲面变化。基于标普500期权的实证分析表明，增强型树基规范在所有预测期限上实现了最低的样本外预测误差，与基准 SHAR 模型相比，一个月前瞻的均方根误差（RMSE）降低了13%。这些改进具有统计显著性，且在压力时期尤为显著。估计出的树结构呈现经济上可解释的分割：短期期权相较于长期期权表现出更高的日度持续性但更低的月度持续性，而深度虚值看涨或看跌期权则展现出与平值期权不同的动态特征。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Hyung Joo Kim and Dong Hwan Oh Despite documented heterogeneity in volatility dynamics across the option surface, standard implied volatility forecasting models apply homogeneous parameters throughout. We introduce a machine-learning framework that uses regression trees to partition the surface along both moneyness and maturity dimensions, identifying data-driven regions where distinct forecasting models perform best. Extending the Surface Heterogeneous Autoregressive (SHAR) framework of Dufays, Jacobs, and Rombouts (2025), we develop tree-based SHAR specifications that preserve interpretable structure while allowing model parameters to vary across the surface. Empirical analysis using S&P 500 options demonstrates that the boosted tree-based specification achieves the lowest out-of-sample forecast errors across all horizons, reducing one-month-ahead RMSE by 13 percent versus the benchmark SHAR model. The improvements are statistically significant and particularly pronounced during stress periods. The estimated tree presents economically interpretable segmentation: short-dated options exhibit higher daily persistence but lower monthly persistence than long-dated options, while deep out-of-the-money calls or puts display distinct dynamics from near-the-money contracts.

</details>

---

_知识库更新时间：2026-07-13T04:30:56.245969_
