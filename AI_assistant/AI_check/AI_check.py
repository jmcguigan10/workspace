import sys

# from optparse import make_option
from pathlib import Path

from provider_name import get_provider

from AI_assistant.AI_check.Config.get_cfg import Load
from AI_assistant.AI_check.Prompt.mk_debug import build_dbg_request
from AI_assistant.AI_check.Prompt.mk_message import make_messages
from AI_assistant.AI_check.Return.write_patch import PatchRunWriter
from AI_assistant.AI_check.utils import check_patch4error, merger, mkodir
from AI_assistant.AI_vendor.utils._ProviderError import ProviderError
from AI_assistant.AI_vendor.utils.api_utils import get_env

# from AI_assistant.utils.arg_parser import check_args


def main(root):
    # Initialize the environment with API key and model specs
    get_env(root)
    args = Load.get_args()
    conf = Load.get_tasks(Path("ai_tasks.yaml"))

    input = {}
    input["root"] = root
    merger(input, args, conf)

    messages = make_messages(input=input)

    try:
        Provider = get_provider(input=input)
        patch_obj = Provider.generate_json(messages, args=input)
        check_patch4error(patch_obj)
    except ProviderError as e:
        print(f"[provider error] {e}", file=sys.stderr)
        sys.exit(3)

    mkodir(input=input)

    dbg_request = build_dbg_request(messages=messages, input=input)

    writer = PatchRunWriter(out_dir=input["output_dir"])
    writer.write_all(dbg_request, patch_obj)
