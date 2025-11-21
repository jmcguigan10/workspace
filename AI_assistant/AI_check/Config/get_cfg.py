import argparse
from pathlib import Path

from omegaconf import OmegaConf


class Load:
    @staticmethod
    def get_tasks(path: Path):
        return OmegaConf.load(path)

    @staticmethod
    def get_args():
        ap = argparse.ArgumentParser(description="Generate AI suggestions (JSON patch)")
        ap.add_argument("--task", default="ai_task.yml", help="Task config YAML")
        ap.add_argument("--prompt", default="prompt.txt", help="Prompt text file")
        ap.add_argument(
            "--out-dir", default=".ai/suggestions", help="Output suggestions dir"
        )
        ap.add_argument(
            "--files",
            default=None,
            help="Optional explicit files (space-separated string)",
        )
        ap.add_argument("--model", default=None, help="Override model id")
        ap.add_argument("--provider", default=None, help="Override provider name")
        return ap.parse_args()
