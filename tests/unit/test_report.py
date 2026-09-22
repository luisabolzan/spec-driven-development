from datetime import date

from src.app.models import Experiment, HardwareProfile, MetricSet
from src.app.report import generate_txt_report


def test_report_includes_optional_metrics_and_hardware_details():
    experiment = Experiment(
        id="EXP-200",
        name="Report check",
        date=date(2026, 9, 22),
        model="MiniCPM-2B",
        dataset="APPS",
        configuration="q4",
        observations="Reasoning harness produced useful traces.",
        hardware=HardwareProfile(cpu="Ryzen 9", gpu="RTX 6000 Ada", ram="48 GB"),
        reasoning_harness=True,
        metrics=MetricSet(pass_at_1=0.73, execution_time_seconds=None, energy_consumption_wh=15.0),
    )

    report = generate_txt_report(experiment)

    assert "Experiment ID: EXP-200" in report
    assert "Reasoning harness used: yes" in report
    assert "- execution_time_seconds: unavailable" in report
    assert "- energy_consumption_wh: 15.0" in report
