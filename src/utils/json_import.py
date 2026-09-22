from __future__ import annotations

import json
from pathlib import Path

from src.app.validation import ValidationError, validate_import_payload


def load_json_experiments(path: str | Path) -> dict:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Import file not found: {file_path}")
    with file_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return validate_import_payload(payload)
