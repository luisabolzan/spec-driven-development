from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional


REQUIRED_FIELDS = ("id", "name", "date", "model")
OPTIONAL_FIELDS = (
    "dataset",
    "quantization_config",
    "hardware_cpu",
    "hardware_gpu",
    "hardware_ram",
    "reasoning_harness_used",
    "notes",
    "pass_at_1",
    "execution_time",
    "energy_consumption",
)


def _coerce_optional(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, str) and value.strip() == "":
        return None
    return value


def _coerce_bool(value: Any) -> Optional[bool]:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"", "not specified", "not available", "unspecified", "unknown"}:
            return None
        if normalized in {"true", "yes", "y", "1"}:
            return True
        if normalized in {"false", "no", "n", "0"}:
            return False
    raise ValueError(f"Invalid boolean value: {value!r}")


def _coerce_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        cleaned = value.strip()
        if cleaned in {"", "not specified", "not available", "unspecified", "unknown"}:
            return None
        return float(cleaned)
    raise ValueError(f"Invalid numeric value: {value!r}")


@dataclass
class Experiment:
    id: str
    name: str
    date: str
    model: str
    dataset: Optional[str] = None
    quantization_config: Optional[str] = None
    hardware_cpu: Optional[str] = None
    hardware_gpu: Optional[str] = None
    hardware_ram: Optional[str] = None
    reasoning_harness_used: Optional[bool] = None
    notes: Optional[str] = None
    pass_at_1: Optional[float] = None
    execution_time: Optional[float] = None
    energy_consumption: Optional[float] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Experiment":
        cleaned = {field: _coerce_optional(data.get(field)) for field in REQUIRED_FIELDS + OPTIONAL_FIELDS}
        cleaned["id"] = str(cleaned.get("id") or "")
        cleaned["name"] = str(cleaned.get("name") or "")
        cleaned["date"] = str(cleaned.get("date") or "")
        cleaned["model"] = str(cleaned.get("model") or "")

        if cleaned.get("reasoning_harness_used") is not None:
            cleaned["reasoning_harness_used"] = _coerce_bool(cleaned["reasoning_harness_used"])
        if cleaned.get("pass_at_1") is not None:
            cleaned["pass_at_1"] = _coerce_float(cleaned["pass_at_1"])
        if cleaned.get("execution_time") is not None:
            cleaned["execution_time"] = _coerce_float(cleaned["execution_time"])
        if cleaned.get("energy_consumption") is not None:
            cleaned["energy_consumption"] = _coerce_float(cleaned["energy_consumption"])

        return cls(**cleaned)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "model": self.model,
        }
        for field in OPTIONAL_FIELDS:
            payload[field] = getattr(self, field)
        return payload


def validate_experiment(experiment: Experiment) -> dict[str, str]:
    errors: dict[str, str] = {}

    if not experiment.name.strip():
        errors["name"] = "Name is required."
    if not experiment.date.strip():
        errors["date"] = "Date is required."
    else:
        try:
            datetime.strptime(experiment.date, "%Y-%m-%d")
        except ValueError:
            errors["date"] = "Date must be a valid YYYY-MM-DD value."
    if not experiment.model.strip():
        errors["model"] = "Model is required."

    for field in ("pass_at_1", "execution_time", "energy_consumption"):
        value = getattr(experiment, field)
        if value is not None:
            try:
                float(value)
            except (TypeError, ValueError):
                errors[field] = f"{field.replace('_', ' ').title()} must be numeric when provided."

    return errors


def format_display_value(value: Any) -> str:
    if value is None:
        return "Not specified"
    if isinstance(value, bool):
        return "Yes" if value else "No"
    return str(value)
