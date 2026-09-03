---
title: "预测低收入国家的债务困境"
paper_id: "worldbank:40125382"
source: "worldbank"
published: "2026-09-02T04:00:00"
score: 80.0
tags: ["paper", "banking-fiscal-monetary-policy"]
---

# 预测低收入国家的债务困境

> **英文原标题**：Predicting Debt Distress in Low-Income Countries

[查看原文](https://documents.worldbank.org/curated/en/099707109022612787)

## 一句话结论

> 该论文开发了一个预测低收入国家债务困境的实证模型，发现简单probit模型优于复杂机器学习算法，并与IMF和世界银行的债务可持续性框架相当。

## 论文信息

- **作者**：-
- **来源**：World Bank Policy Research Working Paper
- **发布时间**：2026-09-02
- **相关度评分**：80.0
- **DOI**：-

## 相关性评分

- **商业银行**：0.0/10
- **货币政策**：0.0/10
- **财政政策**：8.0/10（最高匹配）

<details open>
<summary><strong>中文摘要</strong></summary>

本文构建了一个实证模型，用于预测低收入国家偿债困难（“债务困境”）的发生阶段，并对现有文献作出三项主要贡献。第一，本文开发了更为精细的外部债务困境阶段衡量指标，从而能够更精确地确定困境阶段的起始时间。第二，本文建立了一套系统性算法，利用J-K折交叉验证方法，全面评估超过55万个候选二元预测模型的样本外预测性能。第三，本文检验了更为复杂的机器学习算法是否能够优于简单的probit模型。研究发现，简单的单方程probit模型在预测债务困境方面优于更复杂的算法，并且在预测性能上与重要的政策基准（如国际货币基金组织和世界银行针对低收入国家的债务可持续性框架）相当。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

This paper develops an empirical model to predict episodes of debt servicing difficulties (“debt distress”) in low-income countries, with three main contributions to the existing literature. First, it develops more refined measures of external debt distress episodes that allow timing the onset of distress episodes with increased precision. Second, it develops a systematic algorithm to comprehensively assess the out-of-sample predictive performance of more than 550,000 candidate binary prediction models using J-K-fold cross-validation. Third, it tests whether more sophisticated machine learning algorithms can outperform simple probit models. The paper finds that simple single-equation probit models have better predictive power for debt distress than more sophisticated algorithms and are comparable in terms of predictive performance to important policy benchmarks such as the IMF and World Bank debt sustainability framework for low-income countries.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

本文开发了一个实证模型来预测低收入国家的外部债务困境（债务困境）事件。主要贡献有三：首先，提出了更精确的外部债务困境衡量指标，通过结合直接违约、大量且持续的欠款以及大规模IMF援助来定义困境发作，并利用新数据集更精确地确定困境开始时间。其次，开发了一种系统算法，通过J-K折交叉验证全面评估超过55万个候选二元预测模型的样本外预测性能。第三，测试了更复杂的机器学习算法（如随机森林）是否能优于简单的probit模型。研究发现，简单的单一方程probit模型在预测债务困境方面优于更复杂的算法，并且其预测性能与IMF和世界银行的低收入国家债务可持续性框架等重要政策基准相当。

### 主要创新

- 提出了更精确的外部债务困境衡量指标，结合直接违约、大量且持续的欠款以及大规模IMF援助，并利用新数据集更精确地确定困境开始时间。
- 开发了一种系统算法，通过J-K折交叉验证全面评估超过55万个候选预测模型的样本外预测性能。
- 测试了更复杂的机器学习算法（如随机森林）是否能优于简单的probit模型，发现简单模型表现更好。
- 系统识别了具有强预测性能的模型，并发现即使只有五个或更少变量的简单模型也能达到与复杂模型相当的预测性能。
- 提供了对现有债务困境预测文献的改进，通过更精确的困境定义和更全面的模型评估方法。

### 研究方法

本文采用probit模型作为主要预测模型，并使用J-K折交叉验证评估样本外预测性能。具体步骤包括：定义债务困境事件（未来一年内发生困境），构建包含28个候选预测变量的数据集，通过“暴力”搜索所有相关变量组合（超过55万个模型），并使用交叉验证计算每个模型的损失函数（基于假阳性和假阴性率的二次均值）。此外，还比较了随机森林等机器学习算法。

### 关键结果

研究发现，简单的probit模型在预测债务困境方面优于随机森林等复杂算法。最佳模型通常包含外部债务服务/出口、储备/进口和CPIA等变量。一个仅包含三个变量（CPIA、外部债务服务/出口、储备/进口）的模型具有较好的预测性能。模型性能与模型复杂度之间存在权衡，但增加变量超过一定数量后收益递减。与IMF和世界银行的LIC DSF模型相比，更简单的模型可以达到相当的预测性能。

### 技术栈

- probit模型
- J-K折交叉验证
- 随机森林
- 损失函数（二次均值）
- 标准化边际效应

### 方法优势

- 提出了更精确的债务困境衡量指标，提高了预测的准确性。
- 系统评估了大量模型，提供了全面的模型性能比较。
- 发现简单模型优于复杂模型，为实际应用提供了指导。
- 与政策基准（LIC DSF）进行了比较，具有政策相关性。

### 主要局限

- 样本仅限于低收入国家，可能不适用于其他类型国家。
- 数据覆盖范围有限，部分变量存在测量误差。
- 模型预测性能受限于历史数据，未来可能发生变化。
- 未考虑内生性问题，预测变量可能与债务困境存在反向因果。

### 与当前研究方向的关联

本文与关键词高度相关，涉及商业银行、财政政策、货币政策、公共债务、金融稳定等。研究聚焦于低收入国家的债务困境预测，与公共债务和金融稳定密切相关。方法上使用probit模型和机器学习，属于金融中介和宏观审慎政策领域。

---

_知识库更新时间：2026-09-03T05:02:29.792702_
