import re
from pathlib import Path

# from typing import Any


def discover_files(input):
    # Gather by include globs
    ROOT = input["root"]
    files = set()
    for pat in input["include_globs"] or []:
        for p in ROOT.glob(pat):
            if p.is_file():
                files.add(p)

    # Fallback: if no includes provided, scan repo
    if not files:
        for p in ROOT.rglob("*"):
            if p.is_file():
                files.add(p)

    # Exclude patterns, system junk, and binary-ish suffixes
    def is_excluded(p: Path) -> bool:
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith("__MACOSX/") or "/__MACOSX/" in rel:
            return True
        if p.name.startswith("._"):  # macOS resource fork
            return True
        for pat in input["exclude_globs"] or []:
            import fnmatch

            if fnmatch.fnmatch(rel, pat):
                return True
        if p.suffix.lower() in {
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".pdf",
            ".zip",
            ".bin",
            ".pyc",
        }:
            return True
        return False

    kept = [p for p in files if not is_excluded(p)]
    kept.sort()
    if len(kept) > input["max_files"]:
        kept = kept[: input["max_files"]]
    return kept


def files(input, args) -> None:
    if args.files:
        parts = re.split(r"[\s,]+", args.files)
        explicit_files = [Path(f.strip()) for f in parts if f.strip()]
        input["files"] = [p for p in explicit_files if p.exists() and p.is_file()]
    else:
        limits_conf = input["limits_conf"]
        input["max_files"] = int(limits_conf.max_files)
        input["files"] = discover_files(input)
