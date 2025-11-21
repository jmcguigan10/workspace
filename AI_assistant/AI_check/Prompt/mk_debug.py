from typing import Any, Mapping, Sequence


def build_dbg_request(
    messages: Sequence[Mapping[str, Any]],
    input,
    max_content_chars: int = 1500,
) -> dict:
    """
    Build a debug request payload with messages truncated to a maximum length.

    Truncates each message's `content` field to `max_content_chars` characters and
    appends '...[truncated]' if it was longer.
    """
    return {
        "messages": [
            {
                "role": m["role"],
                "content": (
                    m["content"][:max_content_chars] + "...[truncated]"
                    if len(m["content"]) > max_content_chars
                    else m["content"]
                ),
            }
            for m in messages
        ],
        "model": input["model"],
        "provider": input["provider"],
        "temperature": input["temperature"],
        "max_output_tokens": input["max_output_tokens"],
    }
