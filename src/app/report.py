from __future__ import annotations

from .models import Experiment


def generate_txt_report(experiment: Experiment) -> str:
    metrics = experiment.metrics
    metric_lines = [
        "Metrics:",
        f"- pass@1: {metrics.pass_at_1 if metrics and metrics.pass_at_1 is not None else 'unavailable'}",
        f"- execution_time_seconds: {metrics.execution_time_seconds if metrics and metrics.execution_time_seconds is not None else 'unavailable'}",
        f"- energy_consumption_wh: {metrics.energy_consumption_wh if metrics and metrics.energy_consumption_wh is not None else 'unavailable'}",
    ] if metrics is not None else [
        "Metrics:",
        "- pass@1: unavailable",
        "- execution_time_seconds: unavailable",
        "- energy_consumption_wh: unavailable",
    ]

    lines = [
        f"Experiment ID: {experiment.id}",
        f"Name: {experiment.name}",
        f"Date: {experiment.date.isoformat()}",
        f"Model: {experiment.model}",
        f"Dataset: {experiment.dataset}",
        f"Configuration: {experiment.configuration}",
        f"Observations: {experiment.observations}",
        "Hardware:",
        f"- CPU: {experiment.hardware.cpu}",
        f"- GPU: {experiment.hardware.gpu}",
        f"- RAM: {experiment.hardware.ram}",
        f"Reasoning harness used: {'yes' if experiment.reasoning_harness else 'no'}",
        *metric_lines,
    ]
    return "\n".join(lines) + "\n"
