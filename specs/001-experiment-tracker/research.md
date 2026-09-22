# Research: Experiment Tracker

## Decision Summary

- Decision: Build a local desktop application with a file-backed experiment registry, form-based CRUD, JSON import, and human-readable TXT reports.
- Rationale: The feature is explicitly local, offline, and focused on reliable research tracking rather than remote collaboration or model execution. A desktop app reduces setup friction for individual researchers while keeping the data model simple and auditable.
- Alternatives considered:
  - JSON as primary storage versus SQLite: JSON was chosen because it matches the required import/export contract and keeps the first release simple and transparent.
  - PySide6 versus Tkinter: PySide6 was chosen as the likely default for a more robust GUI toolkit, though Tkinter remains a viable low-dependency alternative if the project prioritizes simplicity over rich controls.
  - Server-backed storage: rejected because the user explicitly requires local-only and no online services.

## Research Findings

### 1. Data model and validation strategy
The app must distinguish between required fields and optional metrics. Required values are the experiment identifier, name, date, model, dataset, quantization/configuration, observations, and hardware profile fields. Optional metrics are allowed to be blank until measured.

### 2. Local persistence approach
A single experiment registry file is sufficient for the first version. This reduces implementation complexity while keeping all records available locally for list, view, edit, and delete workflows. Importing JSON payloads should validate each record before insertion.

### 3. Reporting format
TXT reports should be generated from the stored experiment record and emphasize human readability. The export should include the experiment ID, name, date, model, dataset, configuration, hardware context, reasoning harness flag, observations, and any recorded metrics.

### 4. Validation expectations
The app should validate required fields on save and reject incomplete or malformed records with explicit error messaging. Invalid JSON imports should surface a clear reason without losing the rest of the existing registry.

## Resolved Unknowns

- Project type: desktop application
- Persistence model: local file-based registry
- Validation behavior: required fields must be enforced at the form layer and import layer
- Reporting mode: human-readable TXT export

## Open Operational Notes

The first version deliberately excludes advanced analyses, model execution, and remote synchronization to keep the workflow focused on tracking and evidence preservation.
