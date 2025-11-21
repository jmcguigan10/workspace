import json

import requests
from _ProviderError import ProviderError


class Provider_Output:
    @staticmethod
    def get_output(payload, url, api_key, timeout):
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        r = requests.post(
            url, headers=headers, data=json.dumps(payload), timeout=timeout
        )
        if r.status_code >= 400:
            raise ProviderError(f"OpenAIChat error {r.status_code}: {r.text}")
        return r.json()

    @staticmethod
    def get_text(pre_data):
        try:
            raw = pre_data["choices"][0]["message"]["content"]
            return raw
        except Exception as exc:
            raise ProviderError(
                f"Unexpected response format from model: {json.dumps(pre_data)[:4000]}"
            ) from exc

    @staticmethod
    def get_clean_json(data):
        if "{" in data and "}" in data:
            start = data.find("{")
            end = data.rfind("}")
            if start != -1 and end != -1 and end > start:
                data = data[start : end + 1]
        try:
            return json.loads(data)
        except Exception:
            raise ProviderError(
                f"Failed to parse JSON from model output: {data[:4000]}"
            )
