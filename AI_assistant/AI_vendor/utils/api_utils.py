import os
from pathlib import Path

from _ProviderError import ProviderError


def get_env(root: Path):
    env_path = root / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


class Get_Provider:
    @staticmethod
    def __call__(name: str):
        name = (name or "").strip().lower()
        if name == "openai_chat":
            return OpenAIChatProvider()
        raise ProviderError(
            f"Unknown provider '{name}'. Choose: openai_chat | openai_compatible | anthropic_messages"
        )

    @staticmethod
    def get_api_key() -> str:
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key:
            return api_key
        else:
            raise ProviderError(
                "Missing OPENAI_API_KEY. Put it in .env or your environment."
            )

    @staticmethod
    def get_out_url() -> str:
        url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
        out_url = f"{url.rstrip('/')}/chat/completions"
        return out_url
