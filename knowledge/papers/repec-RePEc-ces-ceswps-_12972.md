---
title: "零样本条件预测与中央银行路径的信息含量"
paper_id: "repec:RePEc:ces:ceswps:_12972"
source: "cesifo"
published: "2026-01-01T00:00:00"
score: 70.0
tags: ["paper", "banking-fiscal-monetary-policy"]
---

# 零样本条件预测与中央银行路径的信息含量

> **英文原标题**：Zero-Shot Conditional Forecasting and the Information Content of Central Bank Paths

[查看原文](https://ideas.repec.org/p/ces/ceswps/_12972.html)

## 一句话结论

> 该论文提出一种零样本条件预测方法，利用预训练的基础时间序列模型读取央行历史预测和未来路径，以评估央行预测路径的信息含量，发现挪威银行和新西兰央行的路径包含额外信息，而瑞典央行则不然。

## 论文信息

- **作者**：Vegard H. Larsen, Leif Anders Thorsrud
- **来源**：CESifo Working Paper Series
- **发布时间**：2026-01-01
- **相关度评分**：70.0
- **DOI**：-

## 相关性评分

- **商业银行**：0.0/10
- **货币政策**：7.0/10（最高匹配）
- **财政政策**：0.0/10

<details open>
<summary><strong>中文摘要</strong></summary>

中央银行会公布预测路径，但这些路径未必是对用于形成预测之信息的最优概括。本文将条件宏观经济预测重新界定为一个输入问题：一个固定的、预训练的多元基础时间序列模型读取该机构的历史预测和已公布的未来路径，连同目标历史数据，而非在局部估计系统内将路径作为与模型一致的约束加以施加。该映射将Mincer-Zarnowitz回归和Granger-Ramanathan回归作为其参数线性特例加以嵌套。仅读取挪威银行公布的路径三元组及目标历史数据，该映射在各预测期限上相对该银行将通胀的均方误差降低，且嵌套组合回归将条件权重赋予映射本身而非路径。一个基于相同未来路径进行硬条件约束、但对预测记录视而不见的VAR模型，在利率和通胀上持续表现逊色，且该结果在能够最优合理化路径的非对称损失设定下依然成立。VAR对比在瑞典和新西兰得到复现；机构间比较仅在新西兰成立，在瑞典至多持平。一个机构学习回归合理化了这一差异：瑞典央行比挪威银行和新西兰储备银行更激进地吸收其近期失误，从而留下较少的残余信号可供提取。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Central banks publish projection paths, but these need not be optimal summaries of the information used to form them. We reframe conditional macroeconomic forecasting as an input problem: a fixed, pre-trained multivariate foundation time-series model reads the institution's historical predictions and announced future paths alongside target histories, rather than imposing the path as a model-consistent restriction inside a locally estimated system. The mapping nests the Mincer-Zarnowitz and Granger-Ramanathan regressions as its parametric-linear special case. Reading just Norges Bank's published path triple and target histories, the map cuts mean squared error against the Bank on inflation across horizons, and the nested combination regression puts the conditional weight on the map, not the path. A hard-conditioned VAR matched on the same future paths, but blind to the prediction record, is consistently outperformed on the rate and inflation, and the result survives the asymmetric-loss specifications that best rationalise the path. The VAR contrast replicates on Sweden and New Zealand; the institutional comparison only on New Zealand, with parity at best on Sweden. An institutional-learning regression rationalises the split: the Riksbank absorbs its recent misses more aggressively than Norges Bank and the RBNZ, leaving less residual signal to extract.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

本文提出将条件宏观预测视为输入问题，利用预训练的多元基础时间序列模型（Chronos-2）读取央行历史预测、公布路径及目标历史，而非在局部估计系统中施加路径约束。该方法嵌套了Mincer-Zarnowitz和Granger-Ramanathan回归作为参数线性特例。实证发现，仅读取挪威央行公布的路径三元组和目标历史，该映射在通胀预测上较央行降低均方误差约21%，且组合回归将条件权重赋予映射而非路径。与硬条件VAR相比，该模型在利率和通胀上表现更优，且结果在非对称损失设定下稳健。在瑞典和新西兰的复制中，新西兰结果与挪威类似，而瑞典未超越央行。机构学习回归表明，瑞典央行更积极地吸收近期失误，留下较少残余信号。

### 主要创新

- 将条件预测重新定义为输入问题，使用预训练基础模型，而非模型约束。
- 证明Mincer-Zarnowitz和Granger-Ramanathan回归是所提框架的线性特例。
- 在多个央行面板上展示零样本条件预测的优越性，并分析跨机构差异。
- 引入“可信度缺口”概念，解释模型与央行路径分歧的预测信息。

### 研究方法

使用Chronos-2基础模型，通过组注意力机制处理多元时间序列，输入包括目标历史、协变量和未来路径。采用递归评估，比较不同输入组合（如仅路径、多元、加外生变量等）的预测精度。使用Diebold-Mariano检验、Mincer-Zarnowitz回归、Granger-Ramanathan组合回归、非对称损失估计（Elliott et al. 2005）和条件VAR对比。

### 关键结果

在挪威，通胀预测的MSE较央行降低约21%（最强输入组）。；在通胀上，组合回归权重偏向模型预测，而政策利率和产出缺口上权重偏向央行路径。；与条件VAR相比，模型在利率和通胀上MSE更低，且多数情况下显著。；新西兰结果与挪威类似，通胀MSE降低高达25%；瑞典未超越央行。；机构学习回归显示，瑞典央行更积极吸收近期失误，导致模型难以超越。

### 技术栈

- Chronos-2（Transformer编码器，组注意力机制）
- Mincer-Zarnowitz回归
- Granger-Ramanathan组合回归
- Diebold-Mariano检验
- Elliott et al. (2005)非对称损失估计（lin-lin和quad-quad）
- 条件VAR（Chan et al. 2025）

### 方法优势

- 提出新颖的输入式条件预测框架，利用预训练模型解决小样本问题。
- 实证设计严谨，包含多种基准和稳健性检验。
- 跨国家比较增强了结论的普遍性。
- 对央行预测效率的讨论具有政策意义。

### 主要局限

- Chronos-2可能受预训练数据污染影响，但作者用合成数据权重验证了稳健性。
- 瑞典结果未超越央行，表明模型适用性有限。
- 未提供所有实验细节，如具体超参数。
- 依赖央行公布的路径，可能受数据修订影响。

### 与当前研究方向的关联

中央银行政策工具：研究央行预测路径的信息含量。；利率与通胀：预测目标包括政策利率和通胀。；宏观审慎政策：涉及央行预测与政策沟通。；金融稳定：预测准确性影响市场预期。

<details>
<summary><strong>发现与关联证据</strong></summary>

- **provider**：IDEAS/RePEc
- **series_url**：https://ideas.repec.org/s/ces/ceswps.html
- **free_download**：True
- **date_precision**：year

</details>

---

_知识库更新时间：2026-09-09T05:10:41.026228_
