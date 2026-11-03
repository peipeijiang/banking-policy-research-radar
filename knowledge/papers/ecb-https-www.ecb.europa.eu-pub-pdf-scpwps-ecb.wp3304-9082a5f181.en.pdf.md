---
title: "欧洲央行对非银行机构的认知：基于机器学习的方法"
paper_id: "ecb:https://www.ecb.europa.eu//pub/pdf/scpwps/ecb.wp3304~9082a5f181.en.pdf"
source: "ecb"
published: "2026-11-02T11:00:00"
score: 70.0
tags: ["paper", "banking-fiscal-monetary-policy"]
---

# 欧洲央行对非银行机构的认知：基于机器学习的方法

> **英文原标题**：ECB perception of non-banks: a machine learning-based approach

[查看原文](https://www.ecb.europa.eu//pub/pdf/scpwps/ecb.wp3304~9082a5f181.en.pdf)

## 一句话结论

> 论文利用微调大语言模型对1998-2025年ECB演讲中关于非银机构的表述进行情绪分类，构建ECB对非银机构感知指数，发现感知总体偏负面且自全球金融危机以来下降，负面情绪主要关联金融稳定与监管关切。

## 论文信息

- **作者**：-
- **来源**：ECB Working Papers
- **发布时间**：2026-11-02
- **相关度评分**：70.0
- **DOI**：-

## 相关性评分

- **商业银行**：4.0/10
- **货币政策**：7.0/10（最高匹配）
- **财政政策**：1.0/10

<details open>
<summary><strong>中文摘要</strong></summary>

本文研究了欧洲中央银行（ECB）对非银行金融中介（NBFIs）的认知，以及这种认知如何被公开传达。我们基于1998至2025年间欧洲央行的演讲构建了一个认知指数。对非银行相关表述的情感倾向，由我们使用为此目的自行构建的手工标注数据集进行微调的大型语言模型进行分类。所得指数揭示出随时间推移总体上偏负面且不断下降的认知，尤其是在全球金融危机之后。负面情感主要与金融稳定和监管需求方面的担忧相关，而正面情感则反映了非银行在促进金融创新和支持市场运行方面的作用。该指数已公开提供以供未来研究使用。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

This paper studies the European Central Bank’s (ECB) perception of non-bank financial intermediaries (NBFIs) and how this perception is publicly communicated. We construct a perception index based on ECB speeches over the period 1998–2025. Sentiment in references to non-banks is classified by a large language model that we fine-tune on our own hand-labeled dataset constructed for this purpose. The resulting index reveals a predominantly negative and declining perception over time, particularly since the Global Financial Crisis. Negative sentiment is primarily associated with concerns related to financial stability and regulatory needs, whereas positive sentiment reflects the role of non-banks in fostering financial innovation and supporting market functioning. The index is made publicly available for future research.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

本文研究欧洲央行（ECB）如何认知非银行金融中介（NBFI）以及如何公开传达这种认知。作者基于1998-2025年ECB演讲构建认知指数，使用大语言模型对涉及非银行的句子进行情感分类，模型在自建的手工标注数据集（1300句）上微调。结果显示，ECB对非银行的认知总体偏负面且随时间下降，尤其在2008年全球金融危机后更为明显。负面情感主要与金融稳定担忧和监管需求相关，正面情感则反映非银行在促进金融创新和支持市场运行方面的作用。指数已公开供后续研究使用。

### 主要创新

- 首次构建量化主要央行对非银行金融部门公开认知的指数，填补了文献空白。
- 采用大语言模型（LLM）对ECB演讲进行句子级情感分类，并针对特定语境手工标注数据微调模型，克服词典方法无法处理上下文和语义反转的局限。
- 将认知指数与具体叙事主题（如监管需求、金融稳定、创新、市场整合）相结合，揭示情感变化背后的经济机制。
- 公开手工标注数据集和认知指数，供后续研究用于基准测试或实证分析。

### 研究方法

论文收集1998年7月至2024年6月ECB的2830篇演讲，分词后得到约31.5万句。首先使用GPT-4o-mini进行主题分类，识别出15017句涉及NBFI的句子（准确率0.93）。然后从全样本中随机选取4000句进行手工标注，其中1300句涉及NBFI，并赋予正面（1）、中性（0）、负面（-1）情感标签。基于该标注数据微调FinBERT、RoBERTa、Llama2 7b-hf、Llama2 13b-hf和Llama3-8B等模型，其中Llama3-8B采用句子级和3句上下文窗口两种设置。选择微调后F1最高的Llama3-8B（窗口-3）对全部NBFI句子进行情感预测。最后按公式（正面句数减负面句数除以总句数）聚合为月度、季度和年度认知指数，并进行稳健性检验（不同上下文大小、参考识别、类别不平衡处理及聚合方法）。

### 关键结果

ECB对非银行的认知总体偏负面，且自全球金融危机以来呈下降趋势，年度指数在危机后几乎完全为负。；存在阶段性正面情感：金融危机前（如1998-2001、2004年）以及2014-2015年监管改革实施后，指数出现正面峰值。；负面情感主要与金融稳定担忧、监管需求、流动性/杠杆风险、银行与非银行互联性及数据缺口相关；近年还涉及加密资产和去中心化金融。；正面情感主要出现在ECB强调非银行促进金融创新、市场整合、多元化及市场运行等贡献时。；微调后Llama3-8B（窗口-3）表现最佳，加权F1为0.80，精确率0.79，召回率0.80；句子级微调F1为0.70。；三个表现最好的模型（微调RoBERTa和两个微调Llama3）的指数动态高度相似，表明指数捕捉到一致的认知。

### 技术栈

- 大语言模型（LLM）：GPT-4o-mini、FinBERT、RoBERTa、Llama2 7b-hf、Llama2 13b-hf、Llama3-8B
- 微调（fine-tuning）
- 句子分词（sentence tokenization）
- TF-IDF向量化（用于词云可视化）
- 情感分类（正面/中性/负面）
- 主题分类
- 聚合公式：Perception = (正面句数 - 负面句数) / 总句数
- 加权精确率、召回率、F1分数评估

### 方法优势

- 创新性地构建了首个量化央行对非银行部门认知的指数，具有方法论贡献。
- 针对特定语境手工标注数据并微调LLM，有效处理了词典方法难以解决的上下文依赖和语义反转问题。
- 结合主题聚类揭示情感变化背后的叙事和经济机制，增强了结果的可解释性。
- 进行了多维度稳健性检验（不同模型、上下文设置、聚合方法），结果稳健。
- 公开标注数据和指数，促进后续研究可复现性和扩展性。

### 主要局限

- 手工标注数据规模有限（1300句用于情感微调），可能影响模型泛化能力。
- 情感标签规则（8条）依赖研究者主观判断，不同标注者间一致性未在文中报告。
- 主题分类使用GPT-4o-mini但未报告其与手工标注的详细对比或误差分析。
- 指数基于ECB演讲，可能无法完全代表ECB官方立场或内部认知。
- 样本期覆盖1998-2025年，但演讲收集截至2024年6月，2025年数据可能不完整。
- 未讨论演讲者身份（如执委 vs. 其他官员）对认知表达的潜在异质性影响。

### 与当前研究方向的关联

本文与研究关键词高度相关。它聚焦中央银行（ECB）的沟通与认知，涉及金融中介（非银行金融中介）、金融稳定（负面情感的主要来源）、宏观审慎政策（监管需求）、信用周期（非银行信贷供给与杠杆的顺周期性）以及货币政策传导（非银行在传导中的作用）。此外，论文采用机器学习方法分析央行文本，属于央行沟通与文本分析的前沿研究，对理解货币政策工具、金融中介结构变化及金融稳定风险具有政策含义。

---

_知识库更新时间：2026-11-03T07:17:21.577070_
