from __future__ import annotations

from datetime import date


class ExperimentForm:
    def __init__(self):
        self.fields = {
            "id": "",
            "name": "",
            "date": "",
            "model": "",
            "dataset": "",
            "configuration": "",
            "observations": "",
            "cpu": "",
            "gpu": "",
            "ram": "",
            "reasoning_harness": False,
            "pass_at_1": "",
            "execution_time_seconds": "",
            "energy_consumption_wh": "",
        }

    def from_data(self, payload: dict) -> None:
        for key, value in payload.items():
            if key in self.fields:
                self.fields[key] = value

    def to_experiment_payload(self) -> dict:
        metrics = {
            "pass_at_1": self._optional_float("pass_at_1"),
            "execution_time_seconds": self._optional_float("execution_time_seconds"),
            "energy_consumption_wh": self._optional_float("energy_consumption_wh"),
        }
        return {
            "id": self.fields["id"],
            "name": self.fields["name"],
            "date": self.fields["date"],
            "model": self.fields["model"],
            "dataset": self.fields["dataset"],
            "configuration": self.fields["configuration"],
            "observations": self.fields["observations"],
            "hardware": {
                "cpu": self.fields["cpu"],
                "gpu": self.fields["gpu"],
                "ram": self.fields["ram"],
            },
            "reasoning_harness": bool(self.fields["reasoning_harness"]),
            "metrics": metrics,
        }

    def _optional_float(self, key: str):
        value = self.fields.get(key, "")
        if value in (None, ""):
            return None
        return float(value)
