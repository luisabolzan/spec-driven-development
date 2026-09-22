import json
import os
import tempfile
import unittest

from experiment_tracker.app import ExperimentTrackerApp
from experiment_tracker.models import Experiment
from experiment_tracker.storage import ExperimentStore


class ExperimentTrackerAppTests(unittest.TestCase):
    def test_app_starts_with_empty_experiment_list(self):
        app = ExperimentTrackerApp(storage_path="temp-empty.json")
        self.assertEqual(app.store.list_experiments(), [])

    def test_store_import_export_round_trip(self):
        temp_dir = tempfile.TemporaryDirectory()
        path = os.path.join(temp_dir.name, "experiments.json")

        store = ExperimentStore()
        store.add_experiment(
            Experiment(
                experiment_id="EXP-0001",
                name="smol-model-qa",
                date="2026-09-22",
                model="TinyLlama-1.1B",
                dataset="HumanEval+",
                configuration="4-bit GPTQ",
                observations="Stable but occasional syntax issues.",
                cpu="Intel i7-12700K",
                gpu="NVIDIA RTX 4090",
                ram="64 GB",
                reasoning_harness=True,
                pass_at_1=72.5,
                execution_time_seconds=18.4,
                energy_consumption_wh=3.2,
            )
        )
        store.export_json(path)

        loaded_store = ExperimentStore()
        loaded_store.import_json(path)

        self.assertEqual(len(loaded_store.list_experiments()), 1)
        self.assertEqual(loaded_store.get_experiment("EXP-0001").name, "smol-model-qa")
        self.assertEqual(loaded_store.get_experiment("EXP-0001").pass_at_1, 72.5)

        temp_dir.cleanup()

    def test_invalid_experiment_data_is_rejected(self):
        errors = ExperimentTrackerApp.validate_experiment_payload({
            "experiment_id": "",
            "name": "",
            "date": "2026/09/22",
            "model": "",
            "dataset": "",
            "configuration": "",
            "cpu": "",
            "gpu": "",
            "ram": "",
            "reasoning_harness": None,
        })
        self.assertTrue(errors)
        self.assertIn("Experiment ID is required.", errors)
        self.assertIn("Date must be in YYYY-MM-DD format.", errors)


if __name__ == "__main__":
    unittest.main()
