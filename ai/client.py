import urllib.request
import urllib.error
import json

API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def ask(system_prompt: str, user_message: str) -> str:
    payload = json.dumps({
        "model": "liquid/lfm-2.5-1.2b-instruct:free",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message}
        ],
        "max_tokens": 512
    }).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Content-Type":  "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            content = data["choices"][0]["message"]["content"]
            if content is None:
                raise RuntimeError("Model returned empty response, it may be overloaded — try again.")
            return content.strip()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        raise RuntimeError(f"API error {e.code}: {body}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e.reason}")