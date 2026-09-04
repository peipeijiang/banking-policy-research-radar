---
title: "Verifiable official statistics: a blockchain-based approach"
paper_id: "repec:RePEc:bis:biswps:1374"
source: "bis_working_papers"
published: "2026-09-01T00:00:00"
score: 0.0
tags: ["paper", "banking-fiscal-monetary-policy"]
---

# Verifiable official statistics: a blockchain-based approach

[查看原文](https://ideas.repec.org/p/bis/biswps/1374.html)

## 一句话结论

> 评分失败，无法生成摘要

## 论文信息

- **作者**：Mario Rusev, Rafael Schmidt, Edward Lambe, Christian Schmieder, Glenn Philip Tice
- **来源**：BIS Working Papers
- **发布时间**：2026-09-01
- **相关度评分**：0.0
- **DOI**：-

## 相关性评分

- **商业银行**：0.0/10
- **货币政策**：0.0/10
- **财政政策**：0.0/10

<details>
<summary><strong>英文摘要</strong></summary>

International organisations including the Bank for International Settlements (BIS) have adopted SDMx (Statistical Data and Metadata) as the standard for exchanging official statistics. Trust in published data is essential for evidence-based policymaking. This paper shows how binding each SDMx dataset to its source using blockchain technology can enhance confidence in official statistics. We present a proof of concept implemented on the XRP Ledger (XRPL) and contribute, as an integrated whole, (i) an SDMx native canonicalisation and per- hashing pipeline; (ii) a domain-separated Merkle aggregation scheme for batched anchoring; (iii) a self-contained, identity-bound verification artefact in which the SDMx message itself carries both the ordered Merkle leaves and a W3C Verifiable Credential signed by a publisher identity key cryptographically bound to the publisher’s XRPL address via an on-chain attestation registry, so that any consumer can re-derive the anchored root and verify the publisher’s identity from the file alone plus a single ledger lookup; (iv) an open-source XRPL-based reference implementation; and (v) a cost model that captures the batch size / latency / fee trade-off and is solved for an economically optimal batch size. The system enables near real-time data verification, provides cryptographic integrity guarantees, and establishes a foundation for future extensions, including zero knowledge proofs and automated verification by AI agents. Measurements on the prototype show median publication latency of 3–5 seconds and verification latency of 1–2 seconds under the controlled test conditions. The approach is data-format-agnostic and can be extended to other structured statistical or regulatory formats.

</details>

<details>
<summary><strong>发现与关联证据</strong></summary>

- **provider**：IDEAS/RePEc
- **series_url**：https://ideas.repec.org/s/bis/biswps.html
- **free_download**：True
- **date_precision**：month

</details>

---

_知识库更新时间：2026-09-04T05:06:46.542852_
