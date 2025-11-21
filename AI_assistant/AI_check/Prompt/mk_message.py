from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def load_schema_hint() -> str:
    """Load the JSON schema instructions from a text file."""
    schema_path = Path(__file__).with_name("schema.txt")
    return schema_path.read_text(encoding="utf-8")


def read_capped(p: Path, max_chars: int) -> str:
    """
    Read text as UTF‑8 (lossy), cap by characters.
    If too long, return head + marker + tail, keeping total length <= max_chars.
    """
    txt = p.read_text(encoding="utf-8", errors="ignore")
    if len(txt) <= max_chars:
        return txt
    half = max_chars // 2
    return txt[:half] + "\n\n# [TRUNCATED]\n...\n\n" + txt[-half:]


def make_messages(input):
    schema_hint = load_schema_hint()
    limits = input["limits_cfg"]

    file_blobs = []
    total = 0
    max_total = int(limits.get("max_total_bytes", 3_000_000))
    per_file = int(limits.get("max_file_bytes", 200_000))

    for p in input["files"]:
        content = read_capped(p, per_file)
        rel = p.relative_to(input["root"]).as_posix()
        blob = f"<<FILE {rel}>>\\n{content}"  # literal "\n" preserved
        size = len(blob.encode("utf-8"))
        if total + size > max_total:
            break
        file_blobs.append(blob)
        total += size

    file_pack = "\\n\\n".join(file_blobs) if file_blobs else "(no files selected)"
    output = input["output"]
    patch_type = output.get("patch_type", "full_text")

    system = (
        "You are an expert software engineer that outputs strict JSON. "
        "Do not include markdown, code fences, comments, or any text outside JSON. "
        f"Default patch_type is '{patch_type}'. "
        "Keep changes minimal and correct. Validate syntax in your head. "
        "\\n\\n"
        f"{schema_hint}"
    )

    user = f"""{input["instructions"]}

    {input["prompt_text"]}

    Files:
    {file_pack}
    """

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


print(load_schema_hint())
