from __future__ import annotations

from typing import Iterable

from .models import Experiment, format_display_value


def generate_txt_report(experiments: Iterable[Experiment]) -> str:
    items = list(experiments)
    lines: list[str] = []

    if not items:
        return "Experiment Tracker Report\n\nNo experiments registered."

    lines.append("Experiment Tracker Report")
    lines.append("=" * 24)
    lines.append("")

    for experiment in items:
        lines.append(f"Experiment ID: {experiment.id}")
        lines.append(f"Name: {format_display_value(experiment.name)}")
        lines.append(f"Date: {format_display_value(experiment.date)}")
        lines.append(f"Model: {format_display_value(experiment.model)}")
        lines.append(f"Dataset: {format_display_value(experiment.dataset)}")
        lines.append(f"Quantization / Configuration: {format_display_value(experiment.quantization_config)}")
        lines.append(f"CPU: {format_display_value(experiment.hardware_cpu)}")
        lines.append(f"GPU: {format_display_value(experiment.hardware_gpu)}")
        lines.append(f"RAM: {format_display_value(experiment.hardware_ram)}")
        lines.append(f"Reasoning Harness Used: {format_display_value(experiment.reasoning_harness_used)}")
        lines.append(f"pass@1: {format_display_value(experiment.pass_at_1)}")
        lines.append(f"Execution Time: {format_display_value(experiment.execution_time)}")
        lines.append(f"Energy Consumption: {format_display_value(experiment.energy_consumption)}")
        lines.append(f"Notes: {format_display_value(experiment.notes)}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"
