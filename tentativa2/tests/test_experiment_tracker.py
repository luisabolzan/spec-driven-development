import json
import unittest
import uuid
from pathlib import Path

from experiment_tracker.models import Experiment, validate_experiment
from experiment_tracker.report import generate_txt_report
from experiment_tracker.storage import ExperimentStore


class ExperimentTests(unittest.TestCase):
    def test_required_fields_are_enforced(self):
        experiment = Experiment(id=str(uuid.uuid4()), name="", date="2026-01-02", model="demo")
        errors = validate_experiment(experiment)
        self.assertIn("name", errors)

    def test_optional_missing_values_are_none(self):
        experiment = Experiment(id=str(uuid.uuid4()), name="Test", date="2026-01-02", model="demo")
        self.assertIsNone(experiment.dataset)
        self.assertIsNone(experiment.hardware_gpu)

    def test_uuid_generation_is_automatic(self):
        experiment = Experiment(id=str(uuid.uuid4()), name="Test", date="2026-01-02", model="demo")
        self.assertTrue(experiment.id)

    def test_report_marks_missing_values_as_unspecified(self):
        experiment = Experiment(id="exp-1", name="Test", date="2026-01-02", model="demo")
        report = generate_txt_report([experiment])
        self.assertIn("Not specified", report)

    def test_store_save_and_load_round_trip(self):
        storage_path = Path("data/test_experiments.json")
        store = ExperimentStore(storage_path)
        experiment = Experiment(
            id="exp-10",
            name="Round Trip",
            date="2026-01-02",
            model="model-x",
            dataset=None,
            hardware_gpu=None,
            pass_at_1=None,
        )
        store.save([experiment])
        loaded = store.load()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].id, "exp-10")
        self.assertIsNone(loaded[0].dataset)

    def test_import_accepts_partial_records(self):
        storage = ExperimentStore(Path("data/test_import.json"))
        payload = [{"id": "exp-2", "name": "Imported", "date": "2026-01-03", "model": "demo-model"}]
        path = Path("data/tmp_import.json")
        path.write_text(json.dumps(payload), encoding="utf-8")
        imported, errors = storage.import_from_json(path)
        self.assertEqual(len(imported), 1)
        self.assertEqual(errors, [])
        path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
