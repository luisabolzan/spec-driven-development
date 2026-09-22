from pathlib import Path

from src.app.models import Experiment, HardwareProfile, MetricSet
from src.app.report import generate_txt_report
from src.app.storage import ExperimentStore
from src.app.validation import ValidationError, validate_experiment_data


def test_end_to_end_experiment_registration_and_report(tmp_path: Path):
    store = ExperimentStore(tmp_path / "experiments.json")
    raw = {
        "id": "EXP-777",
        "name": "Integration run",
        "date": "2026-09-22",
        "model": "Gemma-2-9B",
        "dataset": "MATH",
        "configuration": "q8 + KV cache",
        "observations": "The harness improved reasoning trace clarity.",
        "hardware": {"cpu": "Intel", "gpu": "RTX 4080", "ram": "64 GB"},
        "reasoning_harness": True,
        "metrics": {"pass_at_1": 0.81, "execution_time_seconds": None, "energy_consumption_wh": 18.0},
    }

    experiment = validate_experiment_data(raw)
    store.add_experiment(experiment)

    assert store.get_experiment("EXP-777") is not None
    report = generate_txt_report(store.get_experiment("EXP-777"))
    assert "Integration run" in report
    assert "- execution_time_seconds: unavailable" in report


def test_invalid_import_payload_rejected(tmp_path: Path):
    store = ExperimentStore(tmp_path / "import.json")
    payload = {"wrong_key": []}

    try:
        store.import_experiments(payload)
        raise AssertionError("Expected ValidationError for invalid import payload")
    except ValidationError:
        pass
