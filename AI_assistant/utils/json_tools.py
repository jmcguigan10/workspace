def _clean_json_only(s: str) -> str:
    if "{" in s and "}" in s:
        start = s.find("{")
        end = s.rfind("}")
        if start != -1 and end != -1 and end > start:
            return s[start : end + 1]
    return s
