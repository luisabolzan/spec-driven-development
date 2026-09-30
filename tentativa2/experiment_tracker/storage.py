from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List

from .models import Experiment, REQUIRED_FIELDS, validate_experiment


DEFAULT_STORAGE_PATH = Path(__file__).resolve().parents[1] / "data" / "experiments.json"


class ExperimentStore:
    def __init__(self, storage_path: str | Path | None = None):
        self.storage_path = Path(storage_path) if storage_path is not None else DEFAULT_STORAGE_PATH
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> list[Experiment]:
        if not self.storage_path.exists():
            return []
        try:
            payload = json.loads(self.storage_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []

        if isinstance(payload, dict):
            items = payload.get("experiments", [])
        else:
            items = payload

        experiments: list[Experiment] = []
        for item in items:
            if not isinstance(item, dict):
                continue
            if all(field in item and item.get(field) not in (None, "") for field in REQUIRED_FIELDS):
                experiments.append(Experiment.from_dict(item))
        return experiments

    def save(self, experiments: Iterable[Experiment]) -> None:
        records = [experiment.to_dict() for experiment in experiments]
        payload = {"experiments": records}
        self.storage_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    def add(self, experiment: Experiment) -> None:
        existing = self.load()
        existing.append(experiment)
        self.save(existing)

    def update(self, experiment: Experiment) -> None:
        existing = self.load()
        updated = []
        for item in existing:
            if item.id == experiment.id:
                updated.append(experiment)
            else:
                updated.append(item)
        self.save(updated)

    def delete(self, experiment_id: str) -> None:
        remaining = [item for item in self.load() if item.id != experiment_id]
        self.save(remaining)

    def import_from_json(self, file_path: str | Path) -> tuple[list[Experiment], list[str]]:
        path = Path(file_path)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            return [], [f"Could not read JSON import: {exc}"]

        if isinstance(payload, dict):
            records = payload.get("experiments", [])
        elif isinstance(payload, list):
            records = payload
        else:
            return [], ["Import file must contain a list of experiments or an object with an experiments array."]

        imported: list[Experiment] = []
        validation_errors: list[str] = []
        for index, item in enumerate(records, start=1):
            if not isinstance(item, dict):
                validation_errors.append(f"Record {index}: entry is not an object.")
                continue
            try:
                experiment = Experiment.from_dict(item)
            except ValueError as exc:
                validation_errors.append(f"Record {index}: {exc}")
                continue
            errors = validate_experiment(experiment)
            if errors:
                validation_errors.append(f"Record {index}: invalid required values: {', '.join(errors.values())}")
                continue
            imported.append(experiment)
        return imported, validation_errors
