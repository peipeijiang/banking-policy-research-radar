#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GBRAIN_REPO="${GBRAIN_RESEARCH_REPO:-$HOME/.gbrain/clones/recsys-research}"
WORKERS="${GBRAIN_SYNC_WORKERS:-2}"

if ! command -v gbrain >/dev/null 2>&1; then
  echo "Error: gbrain is not installed or not available in PATH." >&2
  exit 1
fi

if [[ ! -d "$ROOT/knowledge/papers" ]]; then
  echo "Error: paper knowledge directory not found: $ROOT/knowledge/papers" >&2
  exit 1
fi

paper_count="$(find "$ROOT/knowledge/papers" -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')"
if [[ "$paper_count" -eq 0 ]]; then
  echo "Error: no paper Markdown files found in $ROOT/knowledge/papers" >&2
  exit 1
fi

if [[ ! -d "$GBRAIN_REPO/.git" ]]; then
  echo "Error: GBrain research mirror not found: $GBRAIN_REPO" >&2
  echo "Register or clone the recsys-research source first." >&2
  exit 1
fi

if pgrep -f 'gbrain serve' >/dev/null 2>&1; then
  cat >&2 <<'EOF'
GBrain's PGLite database is currently held by `gbrain serve`.
Close Codex/Claude sessions that are using the GBrain MCP server, then run this
script again. PGLite supports one writer, so the script will not force-kill it.
EOF
  exit 2
fi

echo "Syncing research mirror into local GBrain ($paper_count local paper pages)..."
echo "Embedding model: $(gbrain config get embedding_model 2>/dev/null || echo 'configured GBrain default')"

# The registered source tracks the GitHub repository. GBrain pulls it, imports
# only the Git diff, removes deleted pages, and embeds new or changed chunks.
gbrain sync --repo "$GBRAIN_REPO" --workers "$WORKERS" --yes

echo "GBrain sync complete. Try: gbrain query '生成式推荐最近有哪些方法？'"
