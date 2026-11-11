# subfusion

> Based on the Fusion mode of [Atomic Agent](https://github.com/AtomicBot-ai/atomic-agent) (a strong model plans, local workers execute), rebuilt as a Claude Code skill so it runs on a Claude Pro/Max subscription instead of an API key. Unofficial: not affiliated with or endorsed by AtomicBot.

A Claude Code skill that lets Claude plan a task and hand the bulk work to a free local model.

Claude runs on your normal Claude Pro/Max plan inside Claude Code. The local model runs on your own GPU through any OpenAI-compatible server: llama.cpp `llama-server`, Ollama, LM Studio, vLLM. Claude splits the job, sends self-contained subtasks to the local model, checks every result, and merges them. No API key and no extra cost.

Tested with Qwen3.8 27B (`UD-IQ4_XS`) on an RTX 5080, reached from a Mac over Tailscale.

## Install

```bash
git clone https://github.com/niakhais/subfusion.git
mkdir -p ~/.claude/skills
cp -R subfusion/skills/local-worker ~/.claude/skills/
```

The script uses only the Python standard library.

## Start a model server

llama.cpp example (fits a 16 GB GPU):

```bash
llama-server -hf unsloth/Qwen3.8-27B-GGUF:UD-IQ4_XS --port 8080 -ngl 99 -c 32768 -np 1 --no-mmproj --jinja
```

If the server runs on another machine, point the skill at it:

```bash
export LOCAL_WORKER_URL=http://my-pc:8080/v1/chat/completions
```

Default: `http://localhost:8080/v1/chat/completions`. For Ollama use `http://localhost:11434/v1/chat/completions`.

## Use

In Claude Code, ask with the skill in mind:

> use local worker: write unit tests for every function in `app.py`

or type `/local-worker` followed by the task. Claude shows the plan, delegates the bulk parts, reviews and applies the results.

Test the connection directly:

```bash
python3 ~/.claude/skills/local-worker/worker.py "Write a Python function is_prime(n). Code only."
```

## Security

`llama-server` and Ollama have no authentication by default. If the server listens on `0.0.0.0`, restrict it with a firewall to your private network (for example Tailscale's `100.64.0.0/10`) or set an API key. Do not expose it to the internet.

## License

MIT
