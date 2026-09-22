from pathlib import Path

from src.app.models import Experiment, HardwareProfile, MetricSet
from src.app.storage import ExperimentStore


def test_store_round_trip_experiment(tmp_path: Path):
    store = ExperimentStore(tmp_path / "experiments.json")
    experiment = Experiment(
        id="EXP-010",
        name="Round trip",
        date=__import__("datetime").date(2026, 9, 22),
        model="Phi-3-mini",
        dataset="DS-1000",
        configuration="8-bit q4",
        observations="Observation captured.",
        hardware=HardwareProfile(cpu="Intel", gpu="NVIDIA", ram="16 GB"),
        reasoning_harness=True,
        metrics=MetricSet(pass_at_1=0.91, execution_time_seconds=90.2, energy_consumption_wh=7.5),
    )

    store.add_experiment(experiment)
    loaded = store.get_experiment("EXP-010")

    assert loaded is not None
    assert loaded.name == "Round trip"
    assert loaded.metrics.pass_at_1 == 0.91


def test_store_imports_batch_and_keeps_unique_ids(tmp_path: Path):
    store = ExperimentStore(tmp_path / "batch.json")
    payload = {
        "experiments": [
            {
                "id": "EXP-100",
                "name": "Imported run",
                "date": "2026-09-20",
                "model": "Llama-3.2-3B",
                "dataset": "CodeContests",
                "configuration": "q8",
                "observations": "Imported successfully.",
                "hardware": {"cpu": "AMD", "gpu": "RTX", "ram": "32 GB"},
                "reasoning_harness": False,
                "metrics": {"pass_at_1": 0.88, "execution_time_seconds": None, "energy_consumption_wh": None},
            }
        ]
    }

    imported = store.import_experiments(payload)

    assert len(imported) == 1
    assert store.get_experiment("EXP-100") is not None
