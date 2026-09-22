import pytest

from src.app.gui import build_experiment_payload
from src.app.validation import ValidationError


def _fields(**overrides):
    fields = {
        "id": "EXP-GUI",
        "name": "GUI run",
        "date": "2026-09-22",
        "model": "TinyLlama",
        "dataset": "MBPP",
        "configuration": "q4",
        "cpu": "Intel",
        "gpu": "NVIDIA",
        "ram": "32 GB",
        "pass_at_1": "",
        "execution_time_seconds": "",
        "energy_consumption_wh": "",
    }
    fields.update(overrides)
    return fields


def test_gui_payload_preserves_unmeasured_metrics_as_none():
    payload = build_experiment_payload(_fields(pass_at_1="0.75"), "  Notes  ", True)

    assert payload["observations"] == "Notes"
    assert payload["reasoning_harness"] is True
    assert payload["metrics"] == {
        "pass_at_1": 0.75,
        "execution_time_seconds": None,
        "energy_consumption_wh": None,
    }


def test_gui_payload_rejects_non_numeric_metric():
    with pytest.raises(ValidationError, match="execution_time_seconds must be a number"):
        build_experiment_payload(_fields(execution_time_seconds="fast"), "Notes", False)