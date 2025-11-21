import sys
import time
from pathlib import Path
from typing import Any

from which_files import get_files


def txt_to_string(file) -> str:
    try:
        with open(file, "r") as file:
            entire_content = file.read()
    except FileNotFoundError:
        print(f"Error: File '{file}' not found.")
        entire_content = ""
    return entire_content


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

    get_files(input=input, args=args)

    input["temperature"] = float(conf.get("temperature", 0))
    input["max_output_tokens"] = int(conf.get("max_output_tokens", 4000))


def check_patch4error(patch_obj):
    if not isinstance(patch_obj, dict) or "changes" not in patch_obj:
        print(
            f"[error] Model did not return a proper JSON patch object. Got: {str(patch_obj)[:500]}",
            file=sys.stderr,
        )
        sys.exit(4)


def timestamp_id() -> str:
    return time.strftime("%Y-%m-%dT%H-%M-%SZ", time.gmtime())


def mkodir(input):
    run_id = timestamp_id()
    out_dir = Path(input["output_dir"]) / run_id
    out_dir.mkdir(parents=True, exist_ok=True)
