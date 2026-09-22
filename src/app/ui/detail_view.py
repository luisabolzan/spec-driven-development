from __future__ import annotations


class ExperimentDetailView:
    def render(self, experiment: dict) -> dict:
        return {
            "id": experiment.get("id"),
            "name": experiment.get("name"),
            "date": experiment.get("date"),
            "model": experiment.get("model"),
            "dataset": experiment.get("dataset"),
            "configuration": experiment.get("configuration"),
            "observations": experiment.get("observations"),
            "hardware": experiment.get("hardware", {}),
            "reasoning_harness": experiment.get("reasoning_harness"),
            "metrics": experiment.get("metrics"),
        }
