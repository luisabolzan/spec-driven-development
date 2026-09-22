from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .models import Experiment
from .validation import ValidationError, validate_experiment_data, validate_import_payload


class ExperimentStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("{\n  \"experiments\": []\n}\n", encoding="utf-8")

    def _read_payload(self) -> dict:
        with self.path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def _write_payload(self, payload: dict) -> None:
        with self.path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
            handle.write("\n")

    def list_experiments(self) -> list[Experiment]:
        payload = self._read_payload()
        experiments = payload.get("experiments", [])
        return [self._deserialize(exp) for exp in experiments]

    def get_experiment(self, experiment_id: str) -> Experiment | None:
        for experiment in self.list_experiments():
            if experiment.id == experiment_id:
                return experiment
        return None

    def add_experiment(self, experiment: Experiment) -> None:
        payload = self._read_payload()
        existing = payload.get("experiments", [])
        if any(item.get("id") == experiment.id for item in existing):
            raise ValidationError(f"Experiment ID '{experiment.id}' already exists.")
        existing.append(self._serialize(experiment))
        payload["experiments"] = existing
        self._write_payload(payload)

    def update_experiment(self, experiment: Experiment) -> None:
        payload = self._read_payload()
        experiments = payload.get("experiments", [])
        updated = False
        for index, item in enumerate(experiments):
            if item.get("id") == experiment.id:
                experiments[index] = self._serialize(experiment)
                updated = True
                break
        if not updated:
            raise ValidationError(f"Experiment ID '{experiment.id}' does not exist.")
        payload["experiments"] = experiments
        self._write_payload(payload)

    def delete_experiment(self, experiment_id: str) -> None:
        payload = self._read_payload()
        experiments = payload.get("experiments", [])
        filtered = [item for item in experiments if item.get("id") != experiment_id]
        if len(filtered) == len(experiments):
            raise ValidationError(f"Experiment ID '{experiment_id}' does not exist.")
        payload["experiments"] = filtered
        self._write_payload(payload)

    @staticmethod
    def _serialize(experiment: Experiment) -> dict:
        return experiment.to_dict()

    @staticmethod
    def _deserialize(data: dict) -> Experiment:
        return validate_experiment_data(data)

    def import_experiments(self, payload: dict) -> list[Experiment]:
        validated_payload = validate_import_payload(payload)
        imported = []
        for item in validated_payload:
            parsed = validate_experiment_data(item, existing_ids={exp.id for exp in self.list_experiments()})
            self.add_experiment(parsed)
            imported.append(parsed)
        return imported
