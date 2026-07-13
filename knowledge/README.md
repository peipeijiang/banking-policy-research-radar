# Recommender Systems Research Library

This directory is the durable, Git-backed knowledge source for daily papers,
AI analyses, code repositories, user feedback, citation links, and weekly reports.

- `papers/`: one Markdown page per paper
- `index.jsonl`: deduplicated machine-readable paper index
- `graph.json`: OpenAlex citation and related-paper edges
- `feedback.json`: preferences synchronized from GitHub Issues
- `reports/weekly/`: weekly AI research synthesis
- `evidence/`: claim-level evidence packs used to audit weekly reports

## Local GBrain sync

Run the following command from the repository root whenever you want to copy
new or updated paper pages into the local GBrain database:

```bash
./scripts/sync_gbrain.sh
```

The script pulls and incrementally syncs GBrain's `recsys-research` GitHub
mirror. Unchanged papers are skipped, deletions are reconciled, and new or
changed papers are embedded with the model configured in GBrain (the current
local configuration uses `minimax:embo-01`). It does not run the paper
discovery or daily analysis pipeline. Because local GBrain uses the
single-writer PGLite engine, close active Codex/Claude sessions using
`gbrain serve` before running the script from a terminal.

To resend the most recent complete batch from this knowledge index without
fetching new papers:

```bash
WECHAT_WEBHOOK_URL='your-webhook' ./scripts/resend_last_wechat.py
```

Full-text discovery uses lawful copies in this order: ArXiv, OpenAlex repository
locations, Unpaywall, CORE, and public author or institutional repository pages.
