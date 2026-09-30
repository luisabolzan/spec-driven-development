# Requirements Checklist

## Must Have
- Local graphical application for experiment tracking
- Unique experiment identifier
- Experiment creation, listing, viewing, editing, and deletion
- Support for experiment metadata including name, date, model, dataset, configuration, and observations
- Hardware metadata for CPU, GPU, and RAM
- Reasoning harness indicator
- Optional metrics for pass@1, execution time, and energy consumption
- Support for unspecified values and incomplete records
- JSON import
- TXT report generation
- Clear validation and constraint feedback
- Local-only, no-auth, no-remote-service scope

## Scope Boundaries
- No model execution in v1
- No advanced statistical analysis in v1
- No remote synchronization or accounts
- No cloud deployment or online service dependency

## Acceptance Focus
- Users can create, view, update, and delete experiments reliably.
- Missing data does not force placeholder values.
- Validation messaging is understandable and actionable.
- The system remains useful for local research organization and documentation.
