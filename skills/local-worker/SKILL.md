---
name: local-worker
description: Delegate bulk subtasks to a free local model (llama.cpp, Ollama, LM Studio or any OpenAI-compatible server) while Claude plans and reviews. Use when the user says "use the local model", "use local worker", "delegate", or asks Claude to plan and let the local model do the work.
---

# Delegate to a local worker model

Claude is the planner and reviewer. A local model on an OpenAI-compatible server is the worker. The worker costs nothing but is weaker than Claude, so give it well-scoped work and check everything it returns.

## How to run the worker

```bash
python3 ~/.claude/skills/local-worker/worker.py "<self-contained task>"
cat some/file.py | python3 ~/.claude/skills/local-worker/worker.py "<task about this file>"
```

- The worker sees only what you send it. It cannot read files, browse, or see this conversation. Put every needed fact, file excerpt, constraint and the exact output format into the prompt.
- Run worker calls one after another unless the user says their server has several parallel slots.
- Keep each prompt plus expected answer well under the server's context window (often 16k-32k tokens).
- If the script says the model is unreachable, tell the user to start their model server. Do not silently do all the work yourself instead.

## Workflow

1. Plan: break the user's goal into subtasks. Decide which are bulk work suitable for the worker (first drafts, boilerplate, tests, summaries of pasted text, repetitive edits, translations) and which need Claude (architecture, tricky debugging, final decisions, anything security-sensitive).
2. Tell the user the plan in a few lines, marking which parts go to the worker.
3. Delegate each worker subtask with a self-contained prompt.
4. Review every result: check it against the requirements, run code or tests where possible, fix or re-delegate with clearer instructions when it falls short.
5. Merge the results, apply changes yourself, and report what the worker did and what you changed.
