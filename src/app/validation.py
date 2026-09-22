from __future__ import annotations

from datetime import date
from typing import Any

from .models import Experiment, HardwareProfile, MetricSet

REQUIRED_FIELDS = (
    "id",
    "name",
    "date",
    "model",
    "dataset",
    "configuration",
    "observations",
    "hardware",
    "reasoning_harness",
)


class ValidationError(ValueError):
    pass


def _require_non_empty(value: Any, field_name: str) -> None:
    if value is None or (isinstance(value, str) and not value.strip()):
        raise ValidationError(f"{field_name} is required.")


def validate_experiment_data(data: dict, *, existing_ids: set[str] | None = None) -> Experiment:
    existing_ids = existing_ids or set()

    for field_name in REQUIRED_FIELDS:
        if field_name not in data:
            raise ValidationError(f"{field_name} is required.")

    experiment_id = data["id"]
    _require_non_empty(experiment_id, "id")
    if existing_ids and experiment_id in existing_ids:
        raise ValidationError(f"Experiment ID '{experiment_id}' already exists.")

    for field_name in ("name", "model", "dataset", "configuration", "observations"):
        _require_non_empty(data.get(field_name), field_name)

    _require_non_empty(data.get("date"), "date")
    try:
        parsed_date = date.fromisoformat(str(data["date"]))
    except ValueError as exc:
        raise ValidationError("date must be a valid ISO date.") from exc

    hardware_data = data.get("hardware")
    if not isinstance(hardware_data, dict):
        raise ValidationError("hardware is required.")

    for field_name in ("cpu", "gpu", "ram"):
        _require_non_empty(hardware_data.get(field_name), f"hardware.{field_name}")

    reasoning_harness = data.get("reasoning_harness")
    if not isinstance(reasoning_harness, bool):
        raise ValidationError("reasoning_harness must be true or false.")

    metrics_data = data.get("metrics")
    metrics = None
    if metrics_data is not None:
        if not isinstance(metrics_data, dict):
            raise ValidationError("metrics must be an object or null.")
        metrics = MetricSet(
            pass_at_1=metrics_data.get("pass_at_1"),
            execution_time_seconds=metrics_data.get("execution_time_seconds"),
            energy_consumption_wh=metrics_data.get("energy_consumption_wh"),
        )

    return Experiment(
        id=str(experiment_id),
        name=str(data["name"]).strip(),
        date=parsed_date,
        model=str(data["model"]).strip(),
        dataset=str(data["dataset"]).strip(),
        configuration=str(data["configuration"]).strip(),
        observations=str(data["observations"]).strip(),
        hardware=HardwareProfile(
            cpu=str(hardware_data["cpu"]).strip(),
            gpu=str(hardware_data["gpu"]).strip(),
            ram=str(hardware_data["ram"]).strip(),
        ),
        reasoning_harness=reasoning_harness,
        metrics=metrics,
    )


def validate_import_payload(payload: dict) -> list[dict]:
    if not isinstance(payload, dict):
        raise ValidationError("Import payload must be a JSON object.")
    experiments = payload.get("experiments")
    if not isinstance(experiments, list):
        raise ValidationError("Import payload must contain an 'experiments' list.")
    return experiments
