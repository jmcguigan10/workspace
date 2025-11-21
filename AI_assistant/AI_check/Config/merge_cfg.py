import sys
from pathlib import Path
from typing import Any

from get_files import files


def get_model_name(args, conf) -> Any:
    if args.model:
        return args.model
    elif conf.model:
        return conf.model
    else:
        print("Model must be set in ai_task.yaml or via --model", file=sys.stderr)
        sys.exit(2)


# make sure to write input = {} and input["root"] = ROOT before calling make_input()
def merger(input, args, conf) -> None:
    input["prompt_text"] = Path(args.prompt).read_text()
    input["provider_name"] = args.provider
    input["model"] = get_model_name(args, conf)

    input["limits_cfg"] = conf.get("limits", {}) or {}
    input["include_globs"] = conf.get("include", []) or []
    input["exclude_globs"] = conf.get("exclude", []) or []
    input["instructions"] = conf.get("instructions", [])
    input["output"] = conf.get("output", {})

    files(input=input, args=args)

    input["temperature"] = float(conf.get("temperature", 0))
    input["max_output_tokens"] = int(conf.get("max_output_tokens", 4000))
