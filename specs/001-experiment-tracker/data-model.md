# Data Model: Experiment Tracker

## Core Entity: Experiment

An Experiment represents a single recorded research trial or test run.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | Yes | Unique identifier for the experiment. |
| name | string | Yes | Human-readable title of the experiment. |
| date | date | Yes | Date the experiment was recorded or run. |
| model | string | Yes | Model under investigation, including small language models or related variants. |
| dataset | string | Yes | Dataset or corpus used for the experiment. |
| configuration | string | Yes | Quantization or run configuration details. |
| observations | string | Yes | Narrative notes about the run or findings. |
| hardware | HardwareProfile | Yes | CPU, GPU, and RAM details for the environment. |
| reasoning_harness | boolean | Yes | Indicates whether a reasoning-oriented harness was used. |
| metrics | MetricSet | No | Optional recorded measurements. |

## Related Entity: HardwareProfile

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| cpu | string | Yes | CPU model or description. |
| gpu | string | Yes | GPU model or description. |
| ram | string | Yes | Memory capacity or description. |

## Related Entity: MetricSet

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| pass_at_1 | number | No | Pass@1 score when measured. |
| execution_time_seconds | number | No | Runtime duration when measured. |
| energy_consumption_wh | number | No | Energy use when measured. |

## Validation Rules

- id MUST be unique within the local registry.
- name, date, model, dataset, configuration, observations, and hardware details MUST be present before saving a new experiment.
- metrics MUST allow missing values without forcing placeholders or defaults.
- reasoning_harness MUST be explicitly true or false.
- Imported JSON records MUST pass the same validation rules before insertion.

## State/Behavior Notes

- An experiment may be created, viewed, edited, or deleted.
- Metrics may transition from absent to present as measurements become available.
- Deletion removes the experiment from the registry and can no longer be viewed or reported.

## Entity Relationships

- One Experiment contains one HardwareProfile.
- One Experiment may contain zero or one MetricSet.
- A JSON import may create one or more Experiment entries in the local registry.
