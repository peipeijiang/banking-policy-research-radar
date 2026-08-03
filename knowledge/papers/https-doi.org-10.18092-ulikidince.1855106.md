---
title: "货币政策冲击与加密货币收益：基于结构VAR-X分析的证据"
paper_id: "https://doi.org/10.18092/ulikidince.1855106"
source: "openalex"
published: "2026-07-31T00:00:00"
score: 80.0
tags: ["paper", "banking-fiscal-monetary-policy", "Blockchain Technology Applications and Security", "Market Dynamics and Volatility", "Digital Transformation in Financial Services"]
---

# 货币政策冲击与加密货币收益：基于结构VAR-X分析的证据

> **英文原标题**：MONETARY POLICY SHOCKS AND CRYPTOCURRENCY RETURNS: EVIDENCE FROM A STRUCTURAL VAR-X ANALYSIS

[查看原文](https://doi.org/10.18092/ulikidince.1855106)

## 一句话结论

> 使用SVAR-X模型分析2020-2025年美联储利率冲击对五种加密货币收益的短期影响，发现冲击效应显著但短暂且异质。

## 论文信息

- **作者**：Mesut Savrul
- **来源**：Uluslararası İktisadi ve İdari İncelemeler Dergisi
- **发布时间**：2026-07-31
- **相关度评分**：80.0
- **DOI**：[https://doi.org/10.18092/ulikidince.1855106](https://doi.org/10.18092/ulikidince.1855106)

## 相关性评分

- **商业银行**：0.0/10
- **货币政策**：8.0/10（最高匹配）
- **财政政策**：0.0/10

<details open>
<summary><strong>中文摘要</strong></summary>

本研究考察了美国货币政策冲击对加密货币收益率的短期影响，并探讨数字资产是否对传统宏观经济传导机制作出反应。聚焦于2020年后的时期，本文评估了联邦储备委员会利率冲击对比特币（Bitcoin）、以太坊（Ethereum）、索拉纳（Solana）、瑞波币（Ripple）和波场（TRON）的幅度、方向及持续性。分析采用SVAR-X框架，基于2020年1月至2025年12月的日度数据。加密货币对数收益率被设定为内生变量，而美元指数（U.S. Dollar Index）和VIX指数作为外生控制变量纳入模型；联邦基金利率变动被建模为严格外生的政策冲击。脉冲响应结果显示，比特币、以太坊、索拉纳和波场均呈现正向且显著的同期响应，而瑞波币（XRP）则无显著反应。这些效应在数日内消散，表明货币政策传导具有适度、短暂且异质性的特征，而非对加密货币收益率动态产生随时间持续的持久影响。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

This study examines the short-run effects of U.S. monetary policy shocks on cryptocurrency returns and asks whether digital assets respond to conventional macroeconomic transmission mechanisms. Focusing on the post-2020 period, it evaluates the magnitude, direction, and persistence of Federal Reserve rate shocks across Bitcoin, Ethereum, Solana, Ripple, and TRON. The analysis applies an SVAR-X framework to daily data for January 2020-December 2025. Cryptocurrency log returns are treated as endogenous variables, while the U.S. Dollar Index and VIX are included as exogenous controls; federal funds rate changes are modelled as strictly exogenous policy shocks. Impulse-response results show positive and significant contemporaneous responses for Bitcoin, Ethereum, Solana, and TRON, but no significant reaction for XRP. These effects dissipate within days, indicating modest, short-lived, and heterogeneous monetary-policy transmission rather than persistent effects on cryptocurrency return dynamics over time.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

本研究考察了美国货币政策冲击对加密货币收益的短期影响，并探讨数字资产是否对传统宏观经济传导机制作出反应。研究聚焦2020年后时期，评估美联储利率冲击对比特币、以太坊、Solana、瑞波币和TRON的影响大小、方向和持续性。分析采用SVAR-X框架，使用2020年1月至2025年12月的日度数据。加密货币对数收益作为内生变量，美元指数和VIX作为外生控制变量，联邦基金利率变化作为严格外生的政策冲击。脉冲响应结果显示，比特币、以太坊、Solana和TRON对政策冲击有正向且显著的同期反应，而XRP无显著反应。这些效应在几天内消散，表明货币政策传导对加密货币收益动态的影响是短暂且异质的，而非持久性的。

### 主要创新

- 采用SVAR-X模型，将联邦基金利率变化作为严格外生政策冲击，同时控制美元指数和VIX，以分离货币政策效应。
- 同时分析五种主要加密货币（BTC、ETH、SOL、XRP、TRX），揭示资产间的异质性反应。
- 使用日度数据，捕捉货币政策冲击的短期动态效应。
- 通过脉冲响应分析，量化政策冲击的即时影响和持续性。

### 研究方法

研究采用结构向量自回归模型（SVAR-X），其中加密货币对数收益为内生变量，美元指数和VIX为外生控制变量，联邦基金利率变化为外生政策冲击。首先进行ADF单位根检验，确定变量平稳性；然后估计VARX(2)模型，通过信息准则选择滞后阶数；最后通过动态乘数（脉冲响应）分析政策冲击的影响。

### 关键结果

研究发现，联邦基金利率的一个标准差正向冲击导致比特币、以太坊、Solana和TRON的当日收益显著增加约0.2%-0.4%，而XRP无显著反应。这些效应在2-3天内消散，随后围绕零波动。美元指数和VIX的系数大多不显著。Johansen协整检验未发现长期均衡关系，支持使用差分序列。

### 技术栈

- ADF单位根检验
- Johansen协整检验
- VARX模型
- 脉冲响应分析（动态乘数）
- 信息准则（AIC、BIC、HQIC）
- statsmodels库（Python）

### 方法优势

- 使用日度数据，捕捉短期动态效应。
- 同时分析多种加密货币，揭示异质性。
- 控制美元指数和VIX，增强结果稳健性。
- 采用SVAR-X框架，明确外生政策冲击。

### 主要局限

- 日度数据无法捕捉政策公告后的日内调整。
- 样本期（2020-2025）包含异常货币政策环境，可能影响结果普适性。
- 常数参数SVAR-X模型可能无法完全反映加密货币市场敏感性的时变特征。
- 未进行完整结构识别（未指定A和B矩阵），仅使用简化式VARX。

### 与当前研究方向的关联

该研究直接关联货币政策、中央银行政策工具、利率、金融稳定等关键词，通过分析美联储政策对加密货币市场的影响，为货币政策传导机制提供了新证据。

---

_知识库更新时间：2026-08-03T04:13:49.139543_
