# Workspace v2: Local, Approve-First AI Code Editor

A tidy, approve-first workflow that behaves like a local pull request: generate a proposal, review it, then apply guarded changes. This version adds safer filesystem rules, dual virtualenvs, debugging support, and a cleaner Python layout.

### Set API Key environment
```python
get_env(root)
```
### Get ai task configs and input format message.
```python
args = check_args() 
message = txt_to_str(patch_schema.txt)
```
### ———— ↓ ————> send to provider
```python
provider = OpenAIChatProvider()
out = provider.generate_json(message, args)
```

## AI_vendor

### OpenAI and OpenAI Compatible

```python
def _build_payload(
    self,
    messages: List[Dict[str, str]],
    model: str,
    temperature: float,
    max_output_tokens: int,
) -> Dict[str, Any]:
    """Build a payload that works for both OpenAI and OpenAI-compatible APIs.

    OpenAI uses `max_completion_tokens` while many compatible APIs (including
    DeepSeek) expect `max_tokens`. We send both when possible so either
    server can accept the request.
    """
    payload: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "response_format": {"type": "json_object"},
    }

    # Prefer the official OpenAI parameter name but also include the
    # widely-used `max_tokens` for compatibility.
    if max_output_tokens is not None:
        payload["max_tokens"] = max_output_tokens
        # Some OpenAI-compatible servers ignore max_completion_tokens
        payload.setdefault("max_tokens", max_output_tokens)

    return payload
```

### OmegaConf Documentation
[Link](https://omegaconf.readthedocs.io)
