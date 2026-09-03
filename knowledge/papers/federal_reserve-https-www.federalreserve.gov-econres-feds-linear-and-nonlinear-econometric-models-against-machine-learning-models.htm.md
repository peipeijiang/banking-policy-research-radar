---
title: "FEDS Paper: Linear and Nonlinear Econometric Models versus Machine-Learning Models: Evidence from Realized-Volatility Forecasting(Revised)"
paper_id: "federal_reserve:https://www.federalreserve.gov/econres/feds/linear-and-nonlinear-econometric-models-against-machine-learning-models.htm"
source: "federal_reserve"
published: "2026-09-02T15:30:00"
score: 0.0
tags: ["paper", "banking-fiscal-monetary-policy"]
---

# FEDS Paper: Linear and Nonlinear Econometric Models versus Machine-Learning Models: Evidence from Realized-Volatility Forecasting(Revised)

[查看原文](https://www.federalreserve.gov/econres/feds/linear-and-nonlinear-econometric-models-against-machine-learning-models.htm)

## 一句话结论

> 该论文比较了多种计量和机器学习模型在预测已实现波动率上的表现，发现预测效果取决于预测期限，且机器学习模型并未系统性优于计量模型。

## 论文信息

- **作者**：-
- **来源**：Federal Reserve FEDS and IFDP
- **发布时间**：2026-09-02
- **相关度评分**：0.0
- **DOI**：-

## 相关性评分

- **商业银行**：0.0/10（最高匹配）
- **货币政策**：0.0/10
- **财政政策**：0.0/10

<details open>
<summary><strong>中文摘要</strong></summary>

Rehim Kilic 本文考察了哪些持久性和非线性表示对于预测已实现波动率最为有用，以及机器学习是否能在专为长记忆和制度依赖性设计的计量经济学模型之外增添价值。我们针对S&P 500和40只美国股票，将HAR、ARFIMA、阈值HAR、平滑转换HAR和马尔可夫转换HAR与XGBoost及若干神经网络模型进行了比较。模型在基于已实现波动率历史的基准信息集以及由弹性网络（Elastic Net）选择的扩展预测变量集下进行评估。预测性能通过MSFE、MAE、QLIKE、模型置信集（Model Confidence Sets）、Diebold–Mariano检验、已实现效用以及滤波历史模拟VaR和预期损失来评估。结果揭示了稳健的、依赖于预测期限的排序：马尔可夫转换HAR在短期限上表现最佳，ARFIMA通常在月度期限上领先，而五日期限则介于两者之间。机器学习模型有时能改进HAR，但并未系统性地超越更广泛的计量经济学模型集合。这些发现在估计窗口、重新估计频率、更丰富的信息集、对数波动率目标以及个股层面均保持稳健；个股结果对于替代的已实现波动率度量同样稳健。总体而言，预测性能主要取决于捕捉每个期限上最相关的持久性和非线性动态特征。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Rehim Kilic This paper examines which representations of persistence and nonlinearity are most useful for forecasting realized volatility and whether machine learning adds value beyond econometric models designed for long memory and regime dependence. We compare HAR, ARFIMA, threshold HAR, smooth-transition HAR, and Markov-switching HAR with XGBoost and several neural-network models for the S&P 500 and 40 U.S. equities. Models are evaluated under a baseline information set using realized-volatility history and an extended set of predictors selected by Elastic Net. Forecast performance is assessed using MSFE, MAE, QLIKE, Model Confidence Sets, Diebold–Mariano tests, realized utility, and filtered-historical-simulation VaR and expected shortfall. The results reveal a robust horizon-dependent ranking: Markov-switching HAR performs best at short horizons, ARFIMA generally leads at the monthly horizon, and the five-day horizon is intermediate. Machine-learning models sometimes improve on HAR but do not systematically outperform the broader econometric set. These findings are robust across estimation windows, re-estimation frequencies, richer information sets, log-volatility targets, and individual equities; stock-level results are also robust to an alternative realized-volatility measure. Overall, forecast performance depends primarily on capturing the persistence and nonlinear dynamics most relevant at each horizon.

</details>

---

_知识库更新时间：2026-09-03T05:02:29.792302_
