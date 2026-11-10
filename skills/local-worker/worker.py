#!/usr/bin/env python3
"""Send one self-contained subtask to a local OpenAI-compatible model server and print its answer.

Usage:
  worker.py "prompt"                      prompt as argument
  cat file.py | worker.py "review this"   stdin is appended to the prompt as context
  worker.py --max-tokens 4000 "prompt"
Env: LOCAL_WORKER_URL (default http://localhost:8080/v1/chat/completions)
"""
import json
import os
import sys
import urllib.error
import urllib.request

URL = os.environ.get("LOCAL_WORKER_URL", "http://localhost:8080/v1/chat/completions")
SYSTEM = ("You are a worker model. Do exactly the task given, completely. "
          "Return only the result (code, text, or data), no preamble.")


def main(argv):
    max_tokens = 8192
    if len(argv) >= 2 and argv[0] == "--max-tokens":
        max_tokens = int(argv[1])
        argv = argv[2:]
    prompt = " ".join(argv).strip()
    if not sys.stdin.isatty():
        context = sys.stdin.read()
        if context.strip():
            prompt = f"{prompt}\n\n--- context ---\n{context}"
    if not prompt:
        sys.exit("usage: worker.py \"prompt\"  (optionally pipe context on stdin)")

    body = json.dumps({
        "messages": [{"role": "system", "content": SYSTEM},
                     {"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
    }).encode()
    req = urllib.request.Request(URL, body, {"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=900) as r:
            data = json.load(r)
    except urllib.error.URLError as e:
        sys.exit(f"local model unreachable at {URL}: {e}. Is the model server running?")
    except urllib.error.HTTPError as e:
        sys.exit(f"model server error {e.code}: {e.read().decode(errors='replace')[:500]}")

    choice = data["choices"][0]
    print(choice["message"].get("content") or "")
    if choice.get("finish_reason") == "length":
        print("\n[worker: output cut off at max_tokens]", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
