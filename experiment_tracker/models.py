from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional


def generate_experiment_id(existing_ids: set[str] | None = None) -> str:
    existing_ids = existing_ids or set()
    numeric_ids = []
    for experiment_id in existing_ids:
        try:
            if experiment_id.upper().startswith("EXP-"):
                numeric_ids.append(int(experiment_id.split("-")[-1]))
        except ValueError:
            continue

    next_number = max(numeric_ids, default=0) + 1
    return f"EXP-{next_number:04d}"


def _to_optional_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        if value == "":
            return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if number < 0:
        return None
    return number


@dataclass
class Experiment:
    experiment_id: str
    name: str
    date: str
    model: str
    dataset: str
    configuration: str
    observations: str
    cpu: str
    gpu: str
    ram: str
    reasoning_harness: bool
    pass_at_1: Optional[float] = None
    execution_time_seconds: Optional[float] = None
    energy_consumption_wh: Optional[float] = None

    @classmethod
    def blank(cls, experiment_id: str | None = None) -> "Experiment":
        return cls(
            experiment_id=experiment_id or "EXP-0001",
            name="",
            date="",
            model="",
            dataset="",
            configuration="",
            observations="",
            cpu="",
            gpu="",
            ram="",
            reasoning_harness=False,
            pass_at_1=None,
            execution_time_seconds=None,
            energy_consumption_wh=None,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "name": self.name,
            "date": self.date,
            "model": self.model,
            "dataset": self.dataset,
            "configuration": self.configuration,
            "observations": self.observations,
            "cpu": self.cpu,
            "gpu": self.gpu,
            "ram": self.ram,
            "reasoning_harness": self.reasoning_harness,
            "pass_at_1": self.pass_at_1,
            "execution_time_seconds": self.execution_time_seconds,
            "energy_consumption_wh": self.energy_consumption_wh,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Experiment":
        metrics = data.get("metrics", {}) if isinstance(data.get("metrics"), dict) else {}
        return cls(
            experiment_id=str(data.get("experiment_id", "")).strip(),
            name=str(data.get("name", "")).strip(),
            date=str(data.get("date", "")).strip(),
            model=str(data.get("model", "")).strip(),
            dataset=str(data.get("dataset", "")).strip(),
            configuration=str(data.get("configuration", "")).strip(),
            observations=str(data.get("observations", "")).strip(),
            cpu=str(data.get("cpu", "")).strip(),
            gpu=str(data.get("gpu", "")).strip(),
            ram=str(data.get("ram", "")).strip(),
            reasoning_harness=bool(data.get("reasoning_harness", False)),
            pass_at_1=_to_optional_float(data.get("pass_at_1", metrics.get("pass_at_1"))),
            execution_time_seconds=_to_optional_float(
                data.get("execution_time_seconds", metrics.get("execution_time_seconds"))
            ),
            energy_consumption_wh=_to_optional_float(
                data.get("energy_consumption_wh", metrics.get("energy_consumption_wh"))
            ),
        )


def _is_valid_date_string(value: str) -> bool:
    if not value:
        return False
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_experiment_data(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if not str(data.get("experiment_id", "")).strip():
        errors.append("Experiment ID is required.")

    required_fields = {
        "name": "Experiment name is required.",
        "date": "Experiment date is required.",
        "model": "Model is required.",
        "dataset": "Dataset is required.",
        "configuration": "Quantization/configuration is required.",
        "cpu": "CPU information is required.",
        "gpu": "GPU information is required.",
        "ram": "Available RAM is required.",
    }

    for field_name, message in required_fields.items():
        if not str(data.get(field_name, "")).strip():
            errors.append(message)

    if "reasoning_harness" not in data or data.get("reasoning_harness") is None:
        errors.append("Reasoning harness selection is required.")

    if str(data.get("date", "")).strip() and not _is_valid_date_string(str(data["date"]).strip()):
        errors.append("Date must be in YYYY-MM-DD format.")

    metric_checks = {
        "pass_at_1": "pass@1 must be a number between 0 and 100.",
        "execution_time_seconds": "Execution time must be a non-negative number.",
        "energy_consumption_wh": "Energy consumption must be a non-negative number.",
    }

    for field_name, message in metric_checks.items():
        value = data.get(field_name)
        if value in (None, ""):
            continue
        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            errors.append(message)
            continue
        if numeric_value < 0:
            errors.append(message)
            continue
        if field_name == "pass_at_1" and numeric_value > 100:
            errors.append(message)

    return errors
