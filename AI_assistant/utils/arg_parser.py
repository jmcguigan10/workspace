#!/usr/bin/env python3
import argparse


def check_args():
    ap = argparse.ArgumentParser(description="Generate AI suggestions (JSON patch)")
    ap.add_argument("--task", default="ai_task.yml", help="Task config YAML")
    ap.add_argument("--prompt", default="prompt.txt", help="Prompt text file")
    ap.add_argument(
        "--out-dir", default=".ai/suggestions", help="Output suggestions dir"
    )
    ap.add_argument(
        "--files", default=None, help="Optional explicit files (space-separated string)"
    )
    ap.add_argument("--model", default=None, help="Override model id")
    ap.add_argument("--provider", default=None, help="Override provider name")
    return ap.parse_args()


def approve_args():
    ap = argparse.ArgumentParser(description="Apply an AI JSON patch safely")
    ap.add_argument(
        "--patch-dir", required=True, help="Directory containing patch.json"
    )
    ap.add_argument("--repo-root", default=".", help="Repository root (default .)")
    ap.add_argument(
        "--revert-on-failure",
        action="store_true",
        default=True,
        help="Revert all changes if post-apply gates fail",
    )
    ap.add_argument(
        "--no-revert-on-failure", dest="revert_on_failure", action="store_false"
    )
    ap.add_argument(
        "--skip-gates",
        action="store_true",
        help="Skip gates.run_after_apply from ai_task.yml",
    )
    ap.add_argument(
        "--task", default="ai_task.yml", help="Task config YAML (for gates)"
    )
    return ap.parse_args()


def main():
    args = approve_args()
    print(args)
    print(args.task)


if __name__ == "__main__":
    main()
