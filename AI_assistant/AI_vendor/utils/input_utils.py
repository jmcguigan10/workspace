from typing import Any, Dict, List


class Input_Provider:
    @staticmethod
    def get_message(
        messages: List[Dict[str, str]],
        args,
    ) -> Dict[str, Any]:
        message: Dict[str, Any] = {
            "model": args.model,
            "messages": messages,
            "temperature": args.temperature,
            "response_format": {"type": "json_object"},
        }
        if args.max_output_tokens is not None:
            message["max_tokens"] = args.max_output_tokens
            message.setdefault("max_tokens", args.max_output_tokens)

        return message
