import sys
from pathlib import Path

from AI_vendor.utils._ProviderError import ProviderError
from AI_vendor.utils.api_utils import get_env, get_provider

from AI_check.Config.get_cfg import Load
from AI_check.Config.merge_cfg import merger
from AI_check.Prompt.mk_debug import build_dbg_request
from AI_check.Prompt.mk_message import make_messages
from AI_check.Return.write_patch import PatchRunWriter
from AI_check.utils import check_patch4error, mkodir


def main(root) -> None:
    """Entry point for running the AI check pipeline."""
    root = Path(root)

    # Initialize the environment with API key and model specs
    get_env(root)
    args = Load.get_args()

    config_dir = Path(__file__).with_name("Config")
    task_path = config_dir / args.task
    conf = Load.get_tasks(task_path)

    state: dict = {}
    state["root"] = root

    merger(state, args, conf)

    messages = make_messages(state=state)

    try:
        provider = get_provider(state["provider_name"])
        patch_obj = provider.generate_json(messages, args=state)
        check_patch4error(patch_obj)
    except ProviderError as e:
        print(f"[provider error] {e}", file=sys.stderr)
        sys.exit(3)

    mkodir(state=state)

    dbg_request = build_dbg_request(messages=messages, state=state)

    writer = PatchRunWriter(out_dir=state["output_dir"])
    writer.write_all(dbg_request, patch_obj)
