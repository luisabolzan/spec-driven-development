from __future__ import annotations

from pathlib import Path

from .models import Experiment
from .report import generate_txt_report
from .storage import ExperimentStore
from .ui.detail_view import ExperimentDetailView
from .ui.experiment_form import ExperimentForm
from .ui.experiment_list import ExperimentListView
from .validation import ValidationError, validate_experiment_data


class ExperimentTrackerApp:
    def __init__(self, storage_path: str | Path = "experiments.json"):
        self.store = ExperimentStore(storage_path)
        self.form = ExperimentForm()
        self.list_view = ExperimentListView()
        self.detail_view = ExperimentDetailView()

    def save_experiment(self, payload: dict) -> Experiment:
        experiment = validate_experiment_data(payload, existing_ids={item.id for item in self.store.list_experiments()})
        self.store.add_experiment(experiment)
        return experiment

    def update_experiment(self, payload: dict) -> Experiment:
        experiment = validate_experiment_data(payload, existing_ids=set())
        self.store.update_experiment(experiment)
        return experiment

    def delete_experiment(self, experiment_id: str) -> None:
        self.store.delete_experiment(experiment_id)

    def list_experiments(self) -> list[dict]:
        experiments = self.store.list_experiments()
        self.list_view.set_items([experiment.to_dict() for experiment in experiments])
        return self.list_view.render()

    def view_experiment(self, experiment_id: str) -> dict:
        experiment = self.store.get_experiment(experiment_id)
        if experiment is None:
            raise ValidationError(f"Experiment ID '{experiment_id}' does not exist.")
        return self.detail_view.render(experiment.to_dict())

    def export_report(self, experiment_id: str) -> str:
        experiment = self.store.get_experiment(experiment_id)
        if experiment is None:
            raise ValidationError(f"Experiment ID '{experiment_id}' does not exist.")
        return generate_txt_report(experiment)

    def import_experiments(self, payload: dict) -> list[Experiment]:
        return self.store.import_experiments(payload)


def main() -> None:
    from .gui import run_gui

    run_gui()


if __name__ == "__main__":
    main()
