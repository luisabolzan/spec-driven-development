from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from .models import Experiment, generate_experiment_id, validate_experiment_data


class ExperimentStore:
    def __init__(self, experiments: Iterable[Experiment] | None = None) -> None:
        self.experiments: list[Experiment] = []
        for experiment in experiments or []:
            self.add_experiment(experiment)

    def _used_ids(self) -> set[str]:
        return {experiment.experiment_id for experiment in self.experiments}

    def next_experiment_id(self) -> str:
        return generate_experiment_id(self._used_ids())

    def add_experiment(self, experiment: Experiment) -> Experiment:
        if not experiment.experiment_id:
            experiment.experiment_id = self.next_experiment_id()
        elif experiment.experiment_id in self._used_ids():
            raise ValueError(f"Experiment ID {experiment.experiment_id} already exists.")

        self.experiments.append(experiment)
        self.experiments.sort(key=lambda item: item.experiment_id)
        return experiment

    def upsert_experiment(self, experiment: Experiment) -> Experiment:
        for index, existing in enumerate(self.experiments):
            if existing.experiment_id == experiment.experiment_id:
                self.experiments[index] = experiment
                return experiment

        return self.add_experiment(experiment)

    def get_experiment(self, experiment_id: str) -> Experiment | None:
        for experiment in self.experiments:
            if experiment.experiment_id == experiment_id:
                return experiment
        return None

    def delete_experiment(self, experiment_id: str) -> None:
        self.experiments = [experiment for experiment in self.experiments if experiment.experiment_id != experiment_id]

    def list_experiments(self) -> list[Experiment]:
        return sorted(self.experiments, key=lambda item: item.name.lower())

    def export_json(self, file_path: str | Path) -> None:
        payload = [experiment.to_dict() for experiment in self.experiments]
        Path(file_path).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def import_json(self, file_path: str | Path) -> list[Experiment]:
        path = Path(file_path)
        raw_data = json.loads(path.read_text(encoding="utf-8"))

        if isinstance(raw_data, dict):
            raw_data = raw_data.get("experiments", [])

        imported: list[Experiment] = []
        for item in raw_data:
            experiment = Experiment.from_dict(item)
            errors = validate_experiment_data(experiment.to_dict())
            if errors:
                raise ValueError(f"Invalid experiment data in {path.name}: {', '.join(errors)}")
            if not experiment.experiment_id:
                experiment.experiment_id = self.next_experiment_id()
            if experiment.experiment_id in self._used_ids():
                experiment.experiment_id = generate_experiment_id(self._used_ids())
            self.add_experiment(experiment)
            imported.append(experiment)
        return imported

    def to_json(self) -> str:
        return json.dumps([experiment.to_dict() for experiment in self.experiments], indent=2)
