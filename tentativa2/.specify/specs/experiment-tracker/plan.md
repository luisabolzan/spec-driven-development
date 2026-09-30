# Implementation Plan: Experiment Tracker

## 1. Product Goal
Build a lightweight local Python desktop application for organizing experiments involving language models, especially small models used for Python code generation. The application should help a researcher record, browse, review, and report experiments without forcing placeholder values for information that is unknown or unavailable.

The emphasis is on trustworthy research records, not on executing models or performing advanced analytics.

## 2. Product Decisions Carried Forward
The implementation must preserve the following decisions made during clarification:

- The minimum required fields for a saved experiment are identifier, name, date, and model.
- Other experiment information is optional and may remain unspecified when not yet available.
- Missing information must be represented explicitly and consistently without inventing placeholder values.
- Validation should be minimal and focused on data integrity rather than unnecessarily restricting the researcher.
- The primary creation and editing workflow should use a single structured form organized into sections for metadata, hardware, metrics, and notes.
- The interface should be clean, minimal, modern, intuitive, and low-friction.
- Browsing should provide a list of experiments with filtering by model, dataset, and date.
- JSON import should accept partial records when they satisfy the minimum required fields and should preserve missing optional information as unspecified.
- TXT reports should clearly indicate unavailable or unspecified information instead of inventing data.
- Permanent deletion is acceptable for the first version.

## 3. Overall Application Architecture

### 3.1 Architectural approach
Use a small local desktop app architecture with a clear separation between:

- UI layer: graphical form, list, detail view, dialogs, notifications
- Domain layer: entities, validation, import/export logic, report generation
- Persistence layer: local storage for experiment records
- Utilities: ID generation, data normalization, serialization helpers

This keeps the application lightweight and easy to reason about without introducing unnecessary infrastructure.

### 3.2 GUI framework for v1
Use Tkinter as the graphical user interface framework for the first version.

This keeps the application local, lightweight, and easy to maintain while still supporting a clean, modern, low-friction desktop experience that matches the product requirements.

### 3.3 Application structure
A simple modular layout is recommended:

- app/
  - main.py
  - controllers/
  - models/
  - services/
  - ui/
  - storage/
  - utils/

The architecture should remain intentionally compact, with minimal layers and no service-server pattern or distributed components.

## 4. GUI Structure, Navigation, and Visual Organization

### 4.1 Main layout
The application should open to a main workspace with two primary areas:

1. Left panel: experiment list
2. Right panel: selected experiment detail and actions

This creates a familiar desktop layout that supports quick browsing and editing.

### 4.2 Navigation model
Users should be able to:

- open the app and immediately see stored experiments,
- add a new experiment from a primary action,
- filter experiments by model, dataset, and date,
- select an experiment to view its details,
- open an editing form from the selected record,
- delete the selected record with confirmation,
- import JSON data,
- generate a TXT report.

### 4.3 Screen organization
The UI should prioritize readability and low friction:

- experiment list should show compact summary information,
- selected experiment should show full details in a structured layout,
- forms should be separated into sections rather than one long uncontrolled form,
- notes and observations should be visually distinct from structured metadata.

### 4.4 Visual design goals
The interface should be:

- clean and uncluttered,
- modern, with clear hierarchy and spacing,
- minimal but polished,
- comfortable for frequent research logging,
- free of unnecessary decoration or complexity.

### 4.5 Interaction patterns
The app should avoid intrusive validation during typing and instead use:

- inline helper text for optional fields,
- clear error summaries on save,
- confirmation dialogs for destructive actions,
- small hints that indicate a field may be left unspecified.

## 5. Experiment Data Model and Persistence

### 5.1 Core experiment entity
Each experiment should have the following core fields:

Required for save:
- id
- name
- date
- model

Optional fields:
- dataset
- quantization_config
- hardware_cpu
- hardware_gpu
- hardware_ram
- reasoning_harness_used
- observations
- pass_at_1
- execution_time
- energy_consumption

Additional optional metadata may be added later if research needs warrant it, but the first version should keep the model focused and simple.

### 5.2 Data representation rules
The app should preserve explicit missing states using a consistent, minimal pattern such as:

- null for unknown/unset values when supported by the storage model,
- empty string only when appropriate for user-facing form fields,
- a structured explicit status such as "unspecified" when needed for clarity

The important requirement is consistency: missing values must not be converted into invented placeholders such as "N/A" or zeros unless the user explicitly entered them.

### 5.3 Persistence format
Use a local, lightweight persistence mechanism appropriate for a desktop app, such as:

- JSON file-based storage in a local app directory,
- one file for the dataset or a small collection of files for records,
- a simple schema with internal representation unaffected by UI state.

The exact storage format should remain straightforward and local; no database server or external service is needed.

### 5.4 Identifier strategy
Each experiment should receive a unique, stable identifier automatically generated as a UUID. The user should not be required to enter or manually manage an identifier.

## 6. Form Design and Validation

### 6.1 Form structure
The creation and editing workflow should use one structured form divided into sections:

1. Metadata
   - name
   - date
   - model
   - dataset
   - quantization/configuration

2. Hardware
   - CPU
   - GPU
   - RAM

3. Metrics
   - pass@1
   - execution time
   - energy consumption
   - reasoning harness indicator

4. Notes / observations
   - narrative and contextual comments

### 6.2 Form behavior
The form should support:

- Create new experiment
- Edit existing experiment
- Save new or updated record
- Cancel without losing data if a validation issue occurs
- Clear indication of fields that are optional
- Optional fields left blank without warnings unless they are truly required
- Preserve all currently entered values when form validation fails and highlight the fields that require correction

### 6.3 Minimal validation rules
Validation should be intentionally small and focused on integrity:

- required fields must not be empty,
- generated identifiers must be unique,
- date should be a valid date value,
- numeric metrics, when provided, should parse as valid numbers,
- obvious malformed input should be blocked with a clear error message.

### 6.4 Avoiding unnecessary restrictions
The app should not impose:

- arbitrary numeric ranges for all metrics,
- forced placeholders for missing data,
- hard requirements for optional hardware and metrics,
- cross-field constraints that do not materially improve integrity.

The validation strategy should avoid harming exploratory research and should respect the fact that data may be genuinely unavailable.

## 7. Handling Incomplete Experiment Data

### 7.1 Principles
A saved experiment must be valid even when:

- hardware information is unknown,
- dataset is not yet decided,
- model configuration is not later available,
- evaluation metrics are pending,
- notes are still incomplete.

### 7.2 Representation pattern
The app should treat missing data as a first-class state. In practice this means:

- the record may save with null or blank values for optional fields,
- those values should be displayed clearly as unspecified or unavailable,
- the UI should not convert unknown values into misleading defaults.

### 7.3 Data integrity safeguards
The system should still preserve data quality by ensuring:

- required fields are never silently omitted,
- invalid data types are rejected,
- identifier uniqueness is enforced,
- optional missing values remain distinguishable from user-entered values.

## 8. Experiment Listing, Filtering, Viewing, Editing, and Deletion

### 8.1 Experiment list
The list should show a compact summary of each experiment, including at least:

- identifier
- experiment name
- date
- model
- dataset, if available

Additional columns can be included if they remain visually clean and useful.

### 8.2 Filtering
The app should support filtering by:

- model
- dataset
- date

This enables quick review of relevant experimental contexts without introducing heavy analytics features.

### 8.3 Detail view
When an experiment is selected, the app should display its complete record in a clear, read-only summary with sections matching the form structure:

- metadata
- hardware
- metrics
- notes

### 8.4 Editing workflow
The user should be able to edit the selected experiment using the same structured form layout, with fields pre-populated and optional data left as available or unspecified.

### 8.5 Deletion workflow
Deletion should be handled through a confirmation step.

- user selects experiment,
- user chooses delete,
- confirmation dialog asks for explicit confirmation,
- record is removed permanently as per v1 decision.

## 9. JSON Import and Validation

### 9.1 Import behavior
The app should allow importing experiment data from JSON files. It should accept records that satisfy the minimum required fields and preserve optional fields as unspecified when they are missing.

### 9.2 Validation policy for import
Import validation should be intentionally minimal but consistent with the app’s storage rules:

- each record must have a valid identifier, name, date, and model
- invalid JSON syntax should be rejected with a helpful message
- malformed records should be flagged individually or grouped with clear reasons
- missing optional fields should be accepted and preserved, not replaced with invented values

### 9.3 Import result behavior
The app should report import outcomes clearly, such as:

- successful import count,
- number of records skipped due to invalid structure,
- which records had missing optional fields but were accepted.

This keeps the import process useful without being overly rigid.

## 10. TXT Report Generation

### 10.1 Report purpose
The TXT report is intended to support local research documentation and simple sharing. It should be human-readable, clear, and easy to inspect in a text editor or external file viewer.

### 10.2 Report content
The generated report should include all available experiment details, organized by section:

- experiment summary
- metadata
- hardware
- metrics
- observations

### 10.3 Missing information behavior
When fields are missing or unavailable, the report should clearly state that the value is not available or unspecified rather than inventing a value.

Examples:

- Model: unspecified
- GPU: not available
- pass@1: not recorded

This preserves honesty and readability.

### 10.4 Output behavior
The report should be generated as a plain text file, and the app should provide feedback when generation succeeds or fails.

## 11. Automated Tests

### 11.1 Test categories
The project should include automated tests for the core behaviors of the app, focusing on business logic rather than UI pixel-level details.

Recommended test areas:

- experiment creation with required fields
- save rejection when required fields are missing
- preservation of optional unspecified fields
- unique ID generation and uniqueness enforcement
- editing an existing experiment
- deletion confirmation and removal
- filtering by model, dataset, and date
- JSON import acceptance of valid partial records
- JSON import rejection of malformed or incompatible records
- TXT report generation with missing fields
- validation messages for invalid inputs

### 11.2 Test approach
Prefer straightforward unit tests for domain logic and lightweight integration-style tests for file-backed persistence and import/export flows.

The test suite should remain focused on:

- data integrity,
- correct saving and retrieval,
- import/export behavior,
- validation policy,
- report honesty with missing information.

## 12. Scope Boundaries
The plan keeps the project local and lightweight by excluding:

- remote services or account systems,
- authentication or multi-user access,
- cloud synchronization,
- model execution,
- remote inference,
- advanced analytics and visual dashboards,
- infrastructure beyond local storage and app execution.

## 13. Deliverable Milestones

### Milestone 1: Core data model and storage
- define experiment schema
- implement local persistence
- enforce minimal required-field rules
- add explicit missing-value handling

### Milestone 2: Single-form experiment creation and editing
- build metadata form
- build hardware section
- add metrics and notes sections
- implement save/cancel behavior

### Milestone 3: Browsing and viewing
- experiment list
- filtering by model, dataset, and date
- detail view
- delete confirmation flow

### Milestone 4: Import and reporting
- JSON import
- validation messaging
- TXT generation
- report formatting with unspecified values

### Milestone 5: Test coverage and polish
- automated tests for key scenarios
- usability refinements
- final validation against product decisions

## 14. Conclusion
This plan keeps the application focused on dependable local experiment organization rather than execution or analytics. It preserves the clarified decisions that make the app practical and low-friction for research work: minimal required fields, explicit handling of missing data, lightweight validation, clean UI structure, local persistence, simple JSON import, and honest TXT reporting.
