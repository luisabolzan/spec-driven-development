from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class HardwareProfile:
    cpu: str
    gpu: str
    ram: str


@dataclass
class MetricSet:
    pass_at_1: Optional[float] = None
    execution_time_seconds: Optional[float] = None
    energy_consumption_wh: Optional[float] = None


@dataclass
class Experiment:
    id: str
    name: str
    date: date
    model: str
    dataset: str
    configuration: str
    observations: str
    hardware: HardwareProfile
    reasoning_harness: bool
    metrics: Optional[MetricSet] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date.isoformat(),
            "model": self.model,
            "dataset": self.dataset,
            "configuration": self.configuration,
            "observations": self.observations,
            "hardware": {
                "cpu": self.hardware.cpu,
                "gpu": self.hardware.gpu,
                "ram": self.hardware.ram,
            },
            "reasoning_harness": self.reasoning_harness,
            "metrics": (
                {
                    "pass_at_1": self.metrics.pass_at_1,
                    "execution_time_seconds": self.metrics.execution_time_seconds,
                    "energy_consumption_wh": self.metrics.energy_consumption_wh,
                }
                if self.metrics is not None
                else None
            ),
        }
