import json


def mk_output_files(out_dir, dbg_request, patch_obj):
    (out_dir / "request.json").write_text(json.dumps(dbg_request, indent=2))
    (out_dir / "response.json").write_text(json.dumps(patch_obj, indent=2))
    (out_dir / "patch.json").write_text(json.dumps(patch_obj, indent=2))
    (out_dir / "summary.md").write_text(patch_obj.get("summary") or "")
