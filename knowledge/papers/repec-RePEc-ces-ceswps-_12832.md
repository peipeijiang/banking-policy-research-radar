---
title: "主权评级与风险定价：欧盟评级机构的分歧"
paper_id: "repec:RePEc:ces:ceswps:_12832"
source: "cesifo"
published: "2026-01-01T00:00:00"
score: 70.0
tags: ["paper", "banking-fiscal-monetary-policy"]
---

# 主权评级与风险定价：欧盟评级机构的分歧

> **英文原标题**：Sovereign Ratings and Risk Pricing, Agency Divergences in the European Union

[查看原文](https://ideas.repec.org/p/ces/ceswps/_12832.html)

## 一句话结论

> 利用EU-27数据，通过有序probit和机器学习方法，研究主权评级是否反映共同宏观财政基本面，以及评级机构特定偏差是否被市场定价，发现两者均显著影响欧元区国债利差。

## 论文信息

- **作者**：António Afonso, José Alves, Periklis Gogas, Theophilos Papadimitriou
- **来源**：CESifo Working Paper Series
- **发布时间**：2026-01-01
- **相关度评分**：70.0
- **DOI**：-

## 相关性评分

- **商业银行**：0.0/10
- **货币政策**：5.0/10
- **财政政策**：7.0/10（最高匹配）

<details open>
<summary><strong>中文摘要</strong></summary>

基于1995-2024年欧盟27国数据，本文考察了主权评级是否主要反映共同的宏观财政基本面，抑或评级机构偏离该基准的特定差异是否也被纳入主权融资条件。通过混合有序概率模型以及针对惠誉、穆迪和标普的非线性与阈值特征的机器学习诊断层，我们识别出一组稳定的核心评级决定因素，主要包括通货膨胀、债务与GDP之比、经常账户余额、预算平衡规则指标、产出缺口、老年抚养比和收入能力；而国家内部差异较小，主要集中在通货膨胀、债务和失业率方面。机器学习分析证实，灵活模型吸收了基本面与评级之间几乎所有的系统性变化，从而验证了市场定价检验中使用的影子评级分解方法。基于欧洲央行数据的债券收益率回归显示，基本面隐含的影子评级与评级机构特定偏差均被定价于欧元区国债利差中：任一成分每上调一个等级，均与利差降低约50个基点相关。证据表明，这种定价效应随债务上升而增强，且在债务超过GDP的100%后进一步加剧；而较短危机时期的交互效应方向相似但精确度较低。因此，主权评级似乎结合了共同的基本面核心与市场视为具有经济相关信号的自由裁量叠加项。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

Using annual EU-27 data for 1995-2024, we examine whether sovereign ratings mainly reflect common macro-fiscal fundamentals or whether agency-specific departures from that benchmark are also priced into sovereign funding conditions. Pooled ordered probits and a machine-learning diagnostic layer for nonlinearities and thresholds for Fitch, Moody’s, and S&P identify a stable set of core rating determinants centred on inflation, debt-to-GDP, current account balance, budget balance rule indicator, output gap, old-age dependency, and revenue capacity, while within-country variation is narrower and concentrated mainly in inflation, debt, and unemployment. The machine-learning analysis confirms that flexible models absorb nearly all systematic variation between fundamentals and ratings, validating the shadow-rating decomposition used in the market-pricing test. ECB-based bond-yield regressions show that both the fundamentals-implied shadow rating and the agency-specific deviation are priced in euro-area Bund spreads: a one-notch more favourable value of either component is associated with about 50 basis points lower spreads. Evidence indicates that this pricing effect strengthens as debt rises and intensifies further once debt exceeds 100% of GDP, while a shorter crisis-period interaction is directionally similar but less precise. Sovereign ratings therefore appear to combine a common fundamentals core with discretionary overlays that markets treat as economically relevant signals.

</details>

## 深度解读

> 分析依据：**全文深读**

### 核心结论

本文利用1995-2024年欧盟27国年度数据，研究主权评级是否主要反映共同的宏观财政基本面，还是评级机构特有的偏离也被定价到主权融资条件中。通过混合有序Probit模型和机器学习诊断层（随机森林、支持向量机、神经网络、XGBoost），识别出稳定的核心评级决定因素：通胀、债务/GDP、经常账户余额、预算平衡规则指标、产出缺口、老年抚养比和收入能力。机器学习分析证实灵活模型几乎吸收了基本面与评级之间的所有系统变异，验证了市场定价测试中使用的影子评级分解。基于欧洲央行债券收益率的回归显示，基本面隐含的影子评级和机构特定偏离都在欧元区国债利差中被定价：任一成分每改善一个等级，利差约降低50个基点。这种定价效应在债务上升时增强，并在债务超过GDP的100%时进一步加剧。

### 主要创新

- 将评级分解为共同基本面成分和机构特定偏离，并检验两者在主权风险定价中的独立作用。
- 使用机器学习（随机森林、SVM、神经网络、XGBoost）作为诊断工具，验证有序Probit基准是否遗漏非线性或阈值效应。
- 采用时间一致的验证设计，确保模型评估避免前瞻偏差。
- 通过SHAP值和偏依赖图增强机器学习模型的可解释性。
- 发现机构偏离在债务高企时对利差的影响更强，揭示了评级偏离的宏观条件依赖性。

### 研究方法

首先，使用混合有序Probit模型估计各评级机构（惠誉、穆迪、标普）的评级决定因素，构建基本面隐含的影子评级。其次，应用四种机器学习模型（随机森林、支持向量机、神经网络、XGBoost）作为非线性诊断，通过SHAP值和偏依赖图解释特征贡献。然后，将观测评级分解为影子评级和机构偏离。最后，在欧元区样本中，使用包含国家和年份固定效应的面板回归，检验影子评级和机构偏离对10年期国债利差（相对于德国国债）的影响，并加入债务交互项。

### 关键结果

核心评级决定因素包括通胀、债务/GDP、经常账户余额、预算平衡规则指标、产出缺口、老年抚养比和收入能力，这些变量在三个机构中一致显著。；机器学习模型几乎吸收了基本面与评级之间的所有系统变异，验证了有序Probit残差反映的是机构判断而非模型误设。；影子评级和机构偏离每改善一个等级，欧元区国债利差约降低50个基点。；机构偏离的定价效应在债务上升时增强，并在债务超过GDP的100%时进一步加剧。；危机时期的交互项方向相似但估计精度较低。

### 技术栈

- 有序Probit模型
- 随机森林
- 支持向量机
- 神经网络
- XGBoost
- SHAP值
- 偏依赖图
- 面板固定效应回归
- 聚类标准误

### 方法优势

- 将评级分解为共同基本面成分和机构偏离，并检验两者在定价中的独立作用，提供了新的分析视角。
- 使用机器学习作为诊断工具，验证了有序Probit基准的充分性，增强了分解的可信度。
- 采用时间一致的验证设计，避免前瞻偏差。
- 通过SHAP值和偏依赖图增强了机器学习模型的可解释性。
- 样本覆盖欧盟27国长达30年，包含多次危机时期，具有较好的外部有效性。

### 主要局限

- 有序Probit模型假设误差项为标准正态分布，可能不适用于极端尾部事件。
- 机器学习模型虽然拟合良好，但可能过拟合，且其预测能力未在独立测试集上严格评估。
- 市场定价回归可能面临内生性问题，尽管使用了滞后变量，但未采用工具变量等因果识别策略。
- 样本仅限于欧盟国家，结论可能不适用于其他地区。
- 机构偏离的分解依赖于有序Probit的线性指数，可能遗漏更复杂的非线性交互。

### 与当前研究方向的关联

本文直接研究主权评级与风险定价，涉及评级机构行为、主权债券利差、宏观财政基本面，与商业银行、财政政策、货币政策、金融稳定等关键词高度相关。评级影响银行资产负债表和融资条件，财政变量（债务、赤字）是核心决定因素，货币政策通过利率和通胀渠道影响评级，金融稳定则体现在危机时期评级与利差的联动。

<details>
<summary><strong>发现与关联证据</strong></summary>

- **provider**：IDEAS/RePEc
- **series_url**：https://ideas.repec.org/s/ces/ceswps.html
- **free_download**：True
- **date_precision**：year

</details>

---

_知识库更新时间：2026-07-18T03:48:29.407070_
