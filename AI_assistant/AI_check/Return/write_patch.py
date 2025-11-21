import difflib
import json
from pathlib import Path


def synthesize_unified_diff(original_text: str, new_text: str, path: str) -> str:
    a = original_text.splitlines(keepends=True)
    b = new_text.splitlines(keepends=True)
    return "".join(difflib.unified_diff(a, b, fromfile=f"a/{path}", tofile=f"b/{path}"))


class PatchRunWriter:
    """Handle writing all artifacts for a single ai_check run."""

    def __init__(self, out_dir: Path):
        self.out_dir = out_dir

    def write_all(self, dbg_request: dict, patch_obj: dict) -> None:
        """
        Write:
        - request.json   (truncated debug request)
        - response.json  (raw model output)
        - patch.json     (canonical patch)
        - summary.md     (human summary)
        - patch.diff     (optional unified diff, best-effort)
        """
        self._write_core_files(dbg_request, patch_obj)
        self._write_unified_diff(patch_obj)

    def _write_core_files(self, dbg_request: dict, patch_obj: dict) -> None:
        """Write the main JSON + summary artifacts."""
        (self.out_dir / "request.json").write_text(json.dumps(dbg_request, indent=2))
        (self.out_dir / "response.json").write_text(json.dumps(patch_obj, indent=2))
        (self.out_dir / "patch.json").write_text(json.dumps(patch_obj, indent=2))
        (self.out_dir / "summary.md").write_text(patch_obj.get("summary") or "")

    def _write_unified_diff(self, patch_obj: dict) -> None:
        """
        Best-effort unified diff synthesis.

        - For full_text changes, diff old file vs new content.
        - For unified_diff changes, reuse the provided patch text.
        - Writes patch.diff if anything was collected.
        - Swallows all exceptions (matches original behavior).
        """
        try:
            lines = []
            for change in patch_obj.get("changes", []):
                action = change.get("action")
                path = change.get("path")
                if not action or not path:
                    continue
                if action != "modify":
                    continue

                patch_type = change.get("patch_type")

                if patch_type == "full_text" and "content" in change:
                    file_path = Path(path)
                    old_text = file_path.read_text() if file_path.exists() else ""
                    new_text = change["content"]
                    diff = synthesize_unified_diff(old_text, new_text, path)
                    lines.append(diff)
                elif patch_type == "unified_diff" and "patch" in change:
                    lines.append(change["patch"])

            if lines:
                (self.out_dir / "patch.diff").write_text("\n".join(lines))
        except Exception:
            # Keep behavior identical to the inline version: fail silently.
            pass
