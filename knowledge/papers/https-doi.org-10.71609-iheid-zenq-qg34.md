---
title: "实验大型语言模型用于哥伦比亚通货膨胀预测"
paper_id: "https://doi.org/10.71609/iheid-zenq-qg34"
source: "openalex"
published: "2026-08-25T00:00:00"
score: 60.0
tags: ["paper", "banking-fiscal-monetary-policy", "Stock Market Forecasting Methods", "Global Financial Crisis and Policies", "Forecasting Techniques and Applications"]
---

# 实验大型语言模型用于哥伦比亚通货膨胀预测

> **英文原标题**：Experimenting with large language models for inflation forecasting in Colombia

[查看原文](http://repository.graduateinstitute.ch/record/322149)

## 一句话结论

> 本文开发了一个使用大型语言模型实时预测哥伦比亚通胀的框架，通过逐步增加信息集来生成24个月的通胀预测，并评估其与通胀目标的一致性。

## 论文信息

- **作者**：Aaron L. Garavito-Acosta, Edgar Caicedo-Garcia, Wilmer Martinez-Rivera, Juan J. Ospina-Tejeiro
- **来源**：Graduate Institute Geneva Institutional Repository (Graduate Institute of International and Development Studies)
- **发布时间**：2026-08-25
- **相关度评分**：60.0
- **DOI**：[https://doi.org/10.71609/iheid-zenq-qg34](https://doi.org/10.71609/iheid-zenq-qg34)

## 相关性评分

- **商业银行**：0.0/10
- **货币政策**：6.0/10（最高匹配）
- **财政政策**：0.0/10

<details open>
<summary><strong>中文摘要</strong></summary>

本文开发并应用了一个标准化框架，利用大语言模型（LLMs）对哥伦比亚的同比通货膨胀进行预测。我们进行了六个顺序实验，在这些实验中，模型可获得的信息集通过纳入历史宏观经济数据、情境指标、明确的经济结构以及通过网络搜索获取的同期信息而逐步扩展。每种配置均每日执行，并实时生成24个月的通货膨胀预测（而非事后预测），同时提供对预测的定性解释，在更高级的配置中，还包含对影响通货膨胀的冲击的评估。这种实时设计减轻了前视偏差，并产生了真实的预测序列。该框架以Python编程管道的形式实现，调用OpenAI和Google应用程序接口（API），执行预定义的实验特定提示，并自动处理和存储模型响应，同时在更高级的配置中应用预测验证和修订程序。结果表明，更丰富的信息环境产生了更不平滑的通货膨胀路径，这些路径在预测期内保持在3%目标之上，并且与影响通货膨胀的同期国内和外部冲击更为一致。定性分析还表明，模型能够一致地识别相关的通货膨胀驱动因素及其相互作用。这些更丰富的预测路径与基于调查的通货膨胀预期中观察到的模式大体一致。随着更多实时预测序列的可用，将进行正式的预测准确性评估。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

This paper develops and applies a standardized framework for forecasting year-on-year inflation in Colombia using large language models (LLMs). We conduct six sequential experiments in which the information set available to the models is progressively expanded by incorporating historical macroeconomic data, contextual indicators, explicit economic structure, and contemporaneous information retrieved through web search. Each configuration is executed daily and generates 24-month inflation forecasts in real time rather than retrospectively, together with qualitative explanations of the forecasts and, in the more advanced configurations, assessments of the shocks affecting inflation. This real-time design mitigates look-ahead bias and produces genuine forecast vintages. The framework is implemented as a programmatic pipeline in Python that queries the OpenAI and Google APIs, executes predefined experiment-specific prompts, and automatically processes and stores the model responses, while applying forecast validation and revision procedures in the more advanced configurations. The results show that richer information environments produce less monotonic inflation paths that remain above the 3% target over the forecast horizon and are more consistent with the contemporaneous domestic and external shocks affecting inflation. The qualitative analysis also shows that the models consistently identify relevant inflation drivers and their interactions. These richer forecast paths are broadly consistent with the pattern observed in survey-based inflation expectations. A formal evaluation of forecast accuracy will be conducted as additional real-time forecast vintages become available.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

本文开发并应用了一个标准化框架，利用大型语言模型（LLMs）预测哥伦比亚的同比通货膨胀。研究设计了六个顺序实验，逐步扩展模型可获得的信息集，从历史宏观经济数据、背景指标、显式经济结构到通过网页搜索获取的同期信息。每个配置每日运行，实时生成24个月的通货膨胀预测，并附带定性解释和冲击评估。该框架以Python编程管道实现，调用OpenAI和Google API，执行预定义的实验特定提示，并自动处理和存储模型响应。结果显示，更丰富的信息环境产生更少单调的通货膨胀路径，这些路径在预测期内保持在3%目标之上，并与同期国内外冲击更为一致。定性分析表明，模型一致识别出相关的通货膨胀驱动因素及其相互作用。这些更丰富的预测路径与基于调查的通货膨胀预期模式大致一致。正式的预测准确性评估将在更多实时预测样本可用后进行。

### 主要创新

- 开发了六个顺序实验的标准化框架，逐步丰富信息集，以评估LLM预测对信息环境的敏感性。
- 采用实时预测设计，每日生成预测，避免前瞻偏差，产生真实的预测样本。
- 在高级配置中整合了网页搜索获取的同期信息，并进行了冲击评估和一致性验证。
- 提供了可复现的Python管道，实现数据加载、提示构建、模型调用、响应处理和存储。
- 将LLM预测与调查预期进行比较，并分析预测路径的动态和离散度。

### 研究方法

本文采用实验方法，设计六个顺序实验（步骤0-5），逐步增加信息集：步骤0仅使用网页搜索获取的通货膨胀信息；步骤1提供历史通货膨胀序列；步骤2增加汇率、政策利率和GDP增长；步骤3增加背景变量；步骤4引入经济结构（菲利普斯曲线、泰勒规则等）和一致性检查；步骤5增加同期网页信息。使用GPT-4o/GPT-4.1和Gemini 2.5 Pro模型，通过API调用，每日运行，生成24个月预测。高级步骤包含验证和修订程序。

### 关键结果

研究发现，更丰富的信息环境产生更少单调的通货膨胀路径，这些路径保持在3%目标之上，并与同期冲击一致。定性分析显示，模型一致识别出国际油价、全球供应链、国际食品价格等外部因素，以及工资指数化、最低工资、通货膨胀预期等国内因素。预测路径与调查预期模式一致。

### 技术栈

- Python
- Jupyter notebooks
- OpenAI API (GPT-4o, GPT-4.1)
- Google Gemini API (Gemini 2.5 Pro)
- Google Search grounding
- 文本挖掘技术（trigrams）
- 网络分析（word network）

### 方法优势

- 实时预测设计，避免前瞻偏差，产生真实预测样本。
- 系统化的实验框架，逐步增加信息集，清晰评估信息丰富度的影响。
- 结合网页搜索获取同期信息，增强预测的时效性。
- 提供可复现的Python管道，便于其他研究者采用。
- 定性分析提供了对通货膨胀驱动因素的深入理解。

### 主要局限

- 预测准确性评估尚未完成，需要更多实时预测样本。
- 仅使用两个LLM模型（GPT和Gemini），可能限制泛化性。
- 网页搜索信息由Gemini生成，GPT可能未完全对齐。
- 定性分析基于文本挖掘，可能受限于分类准确性。
- 未与传统的计量经济模型进行正式比较。

### 与当前研究方向的关联

该论文直接涉及中央银行政策工具（货币政策）、通货膨胀预测、大型语言模型应用，以及宏观经济预测方法。它探讨了LLM在通货膨胀预测中的潜力，与关键词中的“利率与通胀”、“中央银行政策工具”和“金融稳定”高度相关。

---

_知识库更新时间：2026-08-30T05:47:44.910111_
