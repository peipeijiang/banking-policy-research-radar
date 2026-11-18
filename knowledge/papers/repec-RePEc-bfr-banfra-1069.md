---
title: "挑战美联储？货币政策向稳定币存款利率的传导"
paper_id: "repec:RePEc:bfr:banfra:1069"
source: "banque_de_france"
published: "2026-01-01T00:00:00"
score: 85.0
tags: ["paper", "banking-fiscal-monetary-policy"]
---

# 挑战美联储？货币政策向稳定币存款利率的传导

> **英文原标题**：DeFi-ying the Fed? Monetary Policy Transmission to Stablecoin Deposit Rates

[查看原文](https://ideas.repec.org/p/bfr/banfra/1069.html)

## 一句话结论

> 论文检验美联储货币政策冲击如何传导至美元稳定币在DeFi协议中的存款利率，发现传统短期利率与DeFi存款利率存在持续大价差，短期政策冲击甚至导致反向变动，收敛速度取决于加密价格引发的去杠杆强度与套利渠道的相对力量。

## 论文信息

- **作者**：Andrea Barbon, Jean Barthélemy, Benoît Nguyen
- **来源**：Working papers
- **发布时间**：2026-01-01
- **相关度评分**：85.0
- **DOI**：-

## 相关性评分

- **商业银行**：2.0/10
- **货币政策**：8.5/10（最高匹配）
- **财政政策**：0.5/10

<details open>
<summary><strong>中文摘要</strong></summary>

美联储的货币政策是否影响与美元挂钩的稳定币（stablecoins）利率？尽管主要稳定币发行方不支付利息，但投资者可以通过将稳定币存入去中心化金融（DeFi）协议来获取收益。我们记录了传统短期利率与DeFi存款利率之间异常巨大且持续的利差，以及政策利率变动传导的疲弱与不稳定。我们表明，在短期内，货币政策冲击可能使DeFi存款利率朝与政策利率相反的方向变动，从而延迟了仅在中期内才会出现的趋同。短期效应的方向与趋同速度均取决于加密资产价格反应所引发的去杠杆强度相对于标准利率套利渠道的对比——这一效应受制于投资者在传统金融与去中心化金融之间进行资金桥接的有限能力。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Does the Federal Reserve’s monetary policy influence the rates on USD-pegged stablecoins? While major stablecoin issuers do not pay interest, investors can earn returns by depositing stablecoins in Decentralized Finance (DeFi) protocols. We document unusually large and persistent spreads between traditional short-term interest rates and DeFi deposit rates, as well as a weak and unstable transmission of policy rate changes. We show that, in the short run, monetary policy shocks can move DeFi deposit rates in the opposite direction of policy rates, delaying a convergence that occurs only over the medium run. Both the sign of the short-run effect and the speed of convergence depend on the intensity of deleveraging induced by crypto price reactions relative to the standard interest-rate arbitrage channel -an effect shaped by investors’ limited ability to bridge traditional and decentralized finance.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

本文研究美联储货币政策如何传导至美元稳定币在DeFi协议中的存款利率。作者首先记录四个典型事实：DeFi利率与联邦基金利率存在约100个基点的大幅持续偏离；政策利率变动时DeFi利率常反向变动；DeFi利率与比特币价格高度相关；长期存在均值回归。为解释这些事实，作者构建了一个包含流动性提供者套利与杠杆投资者调整头寸的DeFi借贷模型，并利用Aave链上数据，采用贝叶斯代理VAR识别货币政策冲击。研究发现，短期去杠杆渠道主导，紧缩冲击导致DeFi存款利率下降，随后逐步向长期协整关系收敛；套利渠道因摩擦和大型套利者有限而较弱。微观数据进一步表明，与传统金融联系更紧密的流动性提供者对政策利率反应更强。

### 主要创新

- 首次从理论和实证上系统研究货币政策向DeFi存款利率的传导，并分解出套利渠道与去杠杆渠道。
- 构建了一个包含异质性流动性提供者（传统金融准入不同）和杠杆投资者的简约DeFi借贷模型，可解释短期反向反应与长期收敛。
- 利用高频货币政策意外和贝叶斯代理VAR识别冲击，同时追踪借款需求和稳定币供给的响应。
- 使用钱包级微观数据和双重差分设计，揭示传统金融整合程度对流动性提供者政策反应的影响。
- 记录并解释了DeFi利率与无风险利率之间大幅持续利差的新典型事实。

### 研究方法

论文采用理论建模与实证分析相结合的方法。理论部分构建了一个DeFi借贷模型，其中流动性提供者在传统金融与DeFi之间套利，杠杆投资者根据加密资产预期回报调整借款需求。实证部分使用Aave v2/v3上USDC、USDT、DAI的链上数据，包括聚合时间序列和钱包级头寸数据。识别策略包括：利用FOMC公告附近的高频价格变化作为货币政策冲击，在贝叶斯代理VAR框架下估计冲击对DeFi存款利率、借款需求和稳定币供给的动态影响；使用误差修正模型和协整检验分析长期收敛；通过事件研究（如硅谷银行倒闭）和双重差分设计分析流动性提供者的异质性反应。

### 关键结果

DeFi存款利率与联邦基金利率之间存在大幅持续偏离：2021-2026年平均约高出100个基点，2022年中至2023年底平均低160个基点。；货币政策冲击短期内使DeFi存款利率下降，与政策利率方向相反，随后逐步向长期协整关系收敛，表明短期去杠杆渠道主导。；紧缩冲击减少稳定币供给（套利渠道）并大幅降低DeFi借款需求（去杠杆渠道），后者效应更强。；DeFi利率与比特币回报显著正相关，误差修正模型中比特币回报系数为正且显著。；利差存在显著均值回归，半衰期约为DAI 5周、USDC 4周、USDT 2.2周。；与传统金融整合和合规程度更高的流动性提供者对政策利率反应更强，表明套利渠道受限于大型套利者不足。

### 技术栈

- 贝叶斯代理VAR（Bayesian Proxy-VAR）
- 高频货币政策冲击识别
- 误差修正模型（Error-Correction Model）
- 协整检验（Engle-Granger和Johansen检验）
- 事件研究法
- 双重差分设计（Difference-in-Differences）
- HAC稳健标准误
- 贝叶斯信息准则（BIC）滞后阶数选择

### 方法优势

- 研究问题新颖且具有重要政策意义，连接DeFi与货币政策传导文献。
- 理论模型与实证发现紧密结合，模型能同时解释短期反向反应和长期收敛。
- 使用高频识别策略和链上微观数据，识别较为干净，数据粒度细。
- 多维度实证设计（宏观VAR、事件研究、微观DID）相互印证，稳健性较强。
- 明确刻画了摩擦和投资者异质性在传导中的作用，政策含义清晰。

### 主要局限

- 样本期相对较短（2021-2026），协整和长期收敛结论需谨慎解读。
- 主要基于Aave一个协议，尽管作者认为结论可推广，但外部有效性有待验证。
- 模型为简约模型，可能省略了DeFi生态中其他重要机制（如治理代币激励、跨链套利等）。
- 货币政策冲击识别依赖高频窗口排除其他新闻，但加密市场24/7交易和多重冲击可能干扰识别。
- 钱包级分析中传统金融整合程度的代理变量可能不完全外生。

### 与当前研究方向的关联

本文与货币政策传导、利率、金融中介和金融稳定等关键词高度相关。它直接研究美联储政策利率向新型金融中介（DeFi借贷协议）存款利率的传导，揭示了套利渠道与去杠杆渠道的相互作用，补充了货币政策向非银行金融中介和近货币资产利率传导的文献。同时，论文讨论了稳定币和DeFi对金融稳定的潜在影响，以及传统金融与去中心化金融之间的摩擦，与银行信贷、金融中介、中央银行政策工具和金融稳定等主题紧密相连。

<details>
<summary><strong>发现与关联证据</strong></summary>

- **provider**：IDEAS/RePEc
- **series_url**：https://ideas.repec.org/s/bfr/banfra.html
- **free_download**：True
- **date_precision**：year

</details>

---

_知识库更新时间：2026-11-18T07:57:08.311044_
