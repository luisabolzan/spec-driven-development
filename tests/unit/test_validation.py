from datetime import date

import pytest

from src.app.models import HardwareProfile, MetricSet
from src.app.validation import ValidationError, validate_experiment_data


def test_validate_experiment_data_accepts_valid_record():
    data = {
        "id": "EXP-002",
        "name": "Prompt tune run",
        "date": "2026-09-21",
        "model": "TinyLlama-1.1B",
        "dataset": "MBPP",
        "configuration": "8-bit quantized",
        "observations": "Prompt tuning improved success rate.",
        "hardware": {"cpu": "AMD 7950X", "gpu": "NVIDIA RTX 4090", "ram": "64 GB"},
        "reasoning_harness": False,
        "metrics": {"pass_at_1": 0.82, "execution_time_seconds": 120.0, "energy_consumption_wh": 11.5},
    }

    experiment = validate_experiment_data(data)

    assert experiment.id == "EXP-002"
    assert experiment.date == date(2026, 9, 21)
    assert experiment.hardware.cpu == "AMD 7950X"
    assert experiment.metrics.pass_at_1 == 0.82


def test_validate_experiment_data_requires_missing_fields():
    data = {
        "id": "EXP-003",
        "name": "Missing data",
        "date": "2026-09-20",
        "model": "Gemma-2B",
        "dataset": "HumanEval",
        "configuration": "float16",
        "observations": "",
        "hardware": {"cpu": "Intel", "gpu": "NVIDIA", "ram": "16 GB"},
        "reasoning_harness": True,
    }

    with pytest.raises(ValidationError, match="observations is required"):
        validate_experiment_data(data)


def test_validate_experiment_data_rejects_invalid_date():
    data = {
        "id": "EXP-004",
        "name": "Bad date",
        "date": "not-a-date",
        "model": "Phi-2",
        "dataset": "MBPP",
        "configuration": "q4",
        "observations": "Date is invalid.",
        "hardware": {"cpu": "Intel", "gpu": "NVIDIA", "ram": "8 GB"},
        "reasoning_harness": True,
    }

    with pytest.raises(ValidationError, match="date must be a valid ISO date"):
        validate_experiment_data(data)
