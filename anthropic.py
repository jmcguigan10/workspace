import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from utils.json_tools import _clean_json_only

HERE = Path(__file__).resolve()
ROOT = HERE.parent.parent  # or whatever level up you need
sys.path.append(str(ROOT))


class ProviderError(RuntimeError):
    pass


class AnthropicMessagesProvider:
    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        api_version: Optional[str] = None,
    ):
        self.base_url = base_url or os.environ.get(
            "ANTHROPIC_BASE_URL", "https://api.anthropic.com/v1"
        )
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.api_version = api_version or os.environ.get(
            "ANTHROPIC_VERSION", "2023-06-01"
        )
        if not self.api_key:
            raise ProviderError(
                "Missing ANTHROPIC_API_KEY. Put it in .env or your environment."
            )

    def generate_json(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float,
        max_output_tokens: int,
    ) -> Dict[str, Any]:
        system_parts = [m["content"] for m in messages if m["role"] == "system"]
        user_parts = [m["content"] for m in messages if m["role"] == "user"]
        system = "\n\n".join(system_parts) if system_parts else None
        user = "\n\n".join(user_parts) if user_parts else ""
        url = f"{self.base_url.rstrip('/')}/messages"
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": self.api_version,
            "content-type": "application/json",
        }
        payload: Dict[str, Any] = {
            "model": model,
            "max_tokens": max_output_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": user}],
        }
        if system:
            payload["system"] = system
        r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=120)
        if r.status_code >= 400:
            raise ProviderError(f"Anthropic error {r.status_code}: {r.text}")
        data = r.json()
        text = "".join(
            b.get("text", "")
            for b in data.get("content", [])
            if isinstance(b, dict) and b.get("type") == "text"
        )
        raw = _clean_json_only((text or "").strip())
        try:
            return json.loads(raw)
        except Exception:
            raise ProviderError(f"Failed to parse JSON from model output: {raw[:4000]}")
