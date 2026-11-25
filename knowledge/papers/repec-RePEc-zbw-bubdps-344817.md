---
title: "Some thoughts on modified X-11 seasonal adjustments for time series with complex seasonality"
paper_id: "repec:RePEc:zbw:bubdps:344817"
source: "bundesbank"
published: "2026-01-01T00:00:00"
score: 0.0
tags: ["paper", "banking-fiscal-monetary-policy"]
---

# Some thoughts on modified X-11 seasonal adjustments for time series with complex seasonality

[查看原文](https://ideas.repec.org/p/zbw/bubdps/344817.html)

## 一句话结论

> 论文系统比较了经典X-11与修改版X-11季节调整方法的概念差异，并利用德国月度资本品生产、周度谷歌趋势和日度电力消费等实时数据，实证评估不同趋势周期滤波配置对季节调整信号稳定性和修订特征的影响。

## 论文信息

- **作者**：Webel, Karsten
- **来源**：Discussion Papers
- **发布时间**：2026-01-01
- **相关度评分**：0.0
- **DOI**：10.71734/DP-2026-32

## 相关性评分

- **商业银行**：0.0/10（最高匹配）
- **货币政策**：0.0/10
- **财政政策**：0.0/10

<details open>
<summary><strong>中文摘要</strong></summary>

最近发布的用于官方统计的JDemetra+时间序列软件实现了对经典X-11季节调整方法的改进版本，适用于月度数据和季度数据。尽管这一改进方法能够处理任意周期的季节性数据，但它专门设计用于适应以月内间隔记录的时间序列中常见的特殊性。其主要创新在于实现了丰富的基于核的趋势-循环提取滤波器族，涵盖了传统的Henderson滤波器和Musgrave滤波器，因此改进后的X-11方法本质上是在参数化趋势-循环估计与非参数化季节估计之间迭代切换的混合方法。尽管有这些增强功能，X-11改进版本也对经典例行程序进行了一些简化，主要涉及自动检测和选择程序。因此，改进后的计算例程目前的成熟度尚不明确。为此，我们梳理了两种X-11方法之间的概念差异，并利用德国资本品月度生产的实时数据，在 concurrent revision regime（并行修正机制）下采用不同的季节调整设置，对其影响进行了实证评估。鉴于参数化趋势-循环估计存在众多选项，我们还试图探究不同的趋势-循环滤波器配置是否会导致最终估计信号出现显著差异。为此，我们考虑了实时每周Google趋势数据以及德国的每日电力消费数据，并评估了多种质量标准，如数据驱动的季节滤波器选择的稳定性、与残余季节自相关相关问题的系统性出现情况，以及并行季节调整估计值的修正轮廓。

</details>

<details>
<summary><strong>英文摘要</strong></summary>

A recent release of the JDemetra+ time series software for official statistics imple- ments a modification of the classical X-11 seasonal adjustment approach for monthly and quarterly data. Although this modified method can handle seasonal data with any periodicity, it has been specifically designed to accommodate peculiarities typ- ically seen in time series recorded at sub-monthly intervals. The main novelty is the implementation of rich families of kernel-based trend-cycle extraction filters that encompass the traditional Henderson and Musgrave filters, so that the mod- ified X-11 method is essentially a hybrid switching iteratively between parametric trend-cycle estimation and nonparametric seasonal estimation. Notwithstanding these enhancements, the X-11 modifications also implement some simplifications of the classical routines, which mainly concern automatic detection and selection procedures. Consequently, the current maturity level of the modified computing routines is unclear. We therefore catalogue the conceptual differences between the two X-11 methods and assess their ramifications empirically, using real-time data on monthly production of capital goods in Germany under different seasonal adjust- ment settings in a concurrent revision regime. Given the multitude of options for parametric trend-cycle estimation, we also seek to find out whether different trend- cycle filter configurations provoke significant discrepancies in final estimated signals. To this end, we consider real-time weekly Google trends as well as daily electricity consumption in Germany and evaluate various quality criteria, such as the stability of the data-driven selection of seasonal filters, the systematic occurrence of issues related to remaining seasonal autocorrelation, and the revision profiles of concurrent seasonally adjusted estimates.

</details>

<details>
<summary><strong>发现与关联证据</strong></summary>

- **provider**：IDEAS/RePEc
- **series_url**：https://ideas.repec.org/s/zbw/bubdps.html
- **free_download**：True
- **date_precision**：year

</details>

---

_知识库更新时间：2026-11-25T09:04:24.419062_
