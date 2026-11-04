---
title: "欧洲央行对非银行机构的认知：基于机器学习的方法"
paper_id: "repec:RePEc:ecb:ecbwps:20263304"
source: "ecb_repec"
published: "2026-11-01T00:00:00"
score: 70.0
tags: ["paper", "banking-fiscal-monetary-policy"]
---

# 欧洲央行对非银行机构的认知：基于机器学习的方法

> **英文原标题**：ECB perception of non-banks: a machine learning-based approach

[查看原文](https://ideas.repec.org/p/ecb/ecbwps/20263304.html)

## 一句话结论

> 论文利用大语言模型对1998-2025年ECB演讲进行情绪分类，构建ECB对非银行金融中介的认知指数，发现该认知总体偏负面且自全球金融危机以来持续下降，负面情绪主要与金融稳定和监管担忧相关。

## 论文信息

- **作者**：Tiza Mimun, Anisa, Dalloul, Ami
- **来源**：Working Paper Series
- **发布时间**：2026-11-01
- **相关度评分**：70.0
- **DOI**：-

## 相关性评分

- **商业银行**：4.0/10
- **货币政策**：7.0/10（最高匹配）
- **财政政策**：0.0/10

<details open>
<summary><strong>中文摘要</strong></summary>

本文研究了欧洲中央银行（ECB）对非银行金融中介（NBFIs）的认知以及这种认知如何被公开传达。我们基于1998至2025年间欧洲央行的演讲构建了一个认知指数。对非银行相关表述的情感倾向，由我们利用为此目的自行构建的手工标注数据集微调后的大型语言模型进行分类。所得指数显示，随着时间推移，认知总体偏负面且呈下降趋势，尤其是在全球金融危机之后。负面情感主要与金融稳定和监管需求方面的担忧相关，而正面情感则反映了非银行机构在促进金融创新和支持市场运行方面的作用。该指数已公开提供以供未来研究使用。JEL分类：E44、E52、C80

</details>

<details>
<summary><strong>英文摘要</strong></summary>

This paper studies the European Central Bank’s (ECB) perception of non-bank financial intermediaries (NBFIs) and how this perception is publicly communicated. We construct a perception index based on ECB speeches over the period 1998–2025. Sentiment in references to non-banks is classified by a large language model that we fine-tune on our own hand-labeled dataset constructed for this purpose. The resulting index reveals a predominantly negative and declining perception over time, particularly since the Global Financial Crisis. Negative sentiment is primarily associated with concerns related to financial stability and regulatory needs, whereas positive sentiment reflects the role of non-banks in fostering financial innovation and supporting market functioning. The index is made publicly available for future research. JEL Classification: E44, E52, C80

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

本文研究欧洲央行（ECB）如何认知非银行金融中介（NBFI）并如何公开传达这一认知。作者基于1998-2025年ECB演讲构建认知指数：先识别涉及非银部门的句子，再用大语言模型对情绪进行分类，模型在自建1300句人工标注数据上微调。结果显示，ECB对非银机构的认知总体偏负面且随时间下降，全球金融危机后尤为明显；负面情绪主要与金融稳定和监管需求相关，正面情绪则反映非银机构在金融创新和市场功能方面的作用。指数已公开供后续研究使用。

### 主要创新

- 构建了首个量化主要央行对非银行金融部门公开认知的指数，填补了相关文献空白。
- 采用大语言模型并对自建人工标注数据集进行微调，以捕捉央行沟通中依赖语境的特定情绪含义。
- 将句子级情绪标签聚合为月度/季度/年度认知时间序列，并系统梳理正负面认知背后的叙事主题。
- 公开人工标注数据和认知指数，供后续研究用于基准测试或实证分析。

### 研究方法

收集1998年7月至2024年6月ECB的2830篇演讲，分词后得到约31.54万句。先由GPT-4o-mini进行主题分类，识别出15017句涉及非银部门；再人工标注4000句（其中1300句涉及非银部门）作为训练、验证和测试集。对FinBERT、RoBERTa、Llama2 7b-hf、Llama2 13b-hf和Llama3-8B进行微调，比较句子级和上下文窗口两种设置。最终选用微调后的Llama3-8B（3句上下文窗口）进行情绪分类，并按公式（正面句数减负面句数除以总句数）聚合为认知指数。

### 关键结果

ECB对非银机构的认知总体偏负面，且自全球金融危机以来呈下降趋势，年度层面几乎完全为负面。；季度层面存在阶段性正面回升，如2013年第二季度附近，但未改变整体负面趋势。；负面情绪主要与金融稳定担忧、监管需求、流动性、杠杆、银行与非银互联性、加密资产和数据缺口相关。；正面情绪主要与非银机构促进金融创新、市场整合、分散化和市场功能相关。；微调后Llama3-8B（窗口-3）的加权F1为0.80，优于句子级版本（0.70）和基线模型。；三个表现最好的模型（微调RoBERTa和两个微调Llama-3）动态高度相似，表明指数捕捉到一致的认知。

### 技术栈

- 大语言模型：GPT-4o-mini、FinBERT、RoBERTa、Llama2 7b-hf、Llama2 13b-hf、Llama3-8B
- 微调（fine-tuning）
- 句子级与上下文窗口输入设置
- TF-IDF向量化（用于词云可视化）
- 加权精确率、召回率和F1分数评估
- 按公式聚合句子级情绪为时间序列指数

### 方法优势

- 首次量化主要央行对非银部门的公开认知，具有明确政策含义。
- 针对央行沟通的语境依赖性，采用人工标注加微调LLM的方法，优于词典法和现成模型。
- 进行了多种稳健性检验，包括不同微调设定、聚合方法和模型比较。
- 公开标注数据和指数，便于复现和后续研究。
- 结合主题聚类揭示认知变化背后的叙事和经济机制。

### 主要局限

- 人工标注仅覆盖4000句，其中非银相关1300句，训练数据规模相对有限。
- 情绪标签规则依赖作者对文献和数据的解释，可能存在主观性。
- 指数仅基于ECB演讲，未涵盖其他沟通渠道（如新闻发布会、访谈等）。
- 输入内容未提供模型在全部测试集上的详细分类报告和混淆矩阵完整结果。
- 输入内容未提供指数与其他经济金融变量关系的实证检验。

### 与当前研究方向的关联

本文与中央银行政策工具和金融稳定关键词高度相关：它量化ECB对非银金融中介的认知，涉及金融稳定风险、监管需求、货币政策传导和宏观审慎政策。同时，论文使用机器学习和大语言模型分析央行沟通，属于中央银行沟通与文本分析的前沿方法。与银行信贷和风险承担、资本和流动性监管、金融中介等关键词也有较强关联，因为非银机构与银行的互联性和监管问题是核心叙事之一。

<details>
<summary><strong>发现与关联证据</strong></summary>

- **provider**：IDEAS/RePEc
- **series_url**：https://ideas.repec.org/s/ecb/ecbwps.html
- **free_download**：True
- **date_precision**：month

</details>

---

_知识库更新时间：2026-11-04T06:59:47.218935_
