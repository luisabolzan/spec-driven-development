# Tasks: Experiment Tracker

**Input**: Design documents from `/specs/001-experiment-tracker/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for the local desktop application.

- [x] T001 Create the project directory structure for application code and tests in src/app/, src/utils/, tests/unit/, tests/integration/, and tests/fixtures/
- [x] T002 Initialize the Python project configuration and dependencies for a desktop app in pyproject.toml or requirements.txt
- [x] T003 [P] Configure linting and formatting defaults for Python code in pyproject.toml and editor tooling files

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that must be complete before any user story can be implemented.

**Checkpoint**: The registry model, storage layer, validation rules, and app shell are ready before user story work begins.

- [x] T004 Define the Experiment, HardwareProfile, and MetricSet data structures in src/app/models.py to match the documented data model
- [x] T005 [P] Implement validation rules for required fields, uniqueness, and optional metrics in src/app/validation.py, including the rule that id MUST be unique and required values MUST be present before save
- [x] T006 [P] Implement a local JSON-backed storage layer in src/app/storage.py to create, read, update, delete, and list experiments
- [x] T007 Create the desktop application shell and navigation state in src/app/main.py so the app can open create, list, detail, and edit views

---

## Phase 3: User Story 1 - Register and list experiments (Priority: P1) 🎯 MVP

**Goal**: Researchers can create a valid experiment, view it in the registry, and see clear validation feedback when required data is missing.

**Independent Test**: A researcher can open the app, save a complete experiment, and confirm that the new record appears in the experiment list without submitting invalid data.

### Implementation for User Story 1

- [x] T008 [P] [US1] Add the experiment creation form and required field handling in src/app/ui/experiment_form.py
- [x] T009 [US1] Implement the experiment list view in src/app/ui/experiment_list.py so all registered experiments are displayed
- [x] T010 [US1] Connect the create flow to storage, validation, and list updates in src/app/main.py and src/app/storage.py
- [x] T011 [US1] Add validation messaging for missing or invalid required fields in src/app/validation.py and src/app/ui/experiment_form.py
- [x] T012 [P] [US1] Implement the detail view and selection behavior for a single experiment in src/app/ui/detail_view.py

**Checkpoint**: At this point, User Story 1 is fully functional and testable independently.

---

## Phase 4: User Story 2 - Edit and delete recorded experiments (Priority: P1)

**Goal**: Researchers can update records as experiments evolve and remove outdated entries without losing local context.

**Independent Test**: A researcher can open an existing experiment, change a field such as observations or configuration, save it, and then delete the record while the local registry remains consistent.

### Implementation for User Story 2

- [x] T013 [P] [US2] Add edit-mode behavior and pre-populated form values in src/app/ui/experiment_form.py
- [x] T014 [US2] Implement save/update logic for existing experiments in src/app/storage.py and src/app/main.py
- [x] T015 [US2] Implement delete workflow and confirmation handling in src/app/ui/detail_view.py and src/app/main.py
- [x] T016 [US2] Ensure unmeasured optional metrics remain blank instead of forcing a placeholder value in src/app/models.py and src/app/validation.py

**Checkpoint**: At this point, the registry supports full lifecycle management for experiments.

---

## Phase 5: User Story 3 - Import JSON and generate TXT reports (Priority: P2)

**Goal**: Researchers can import existing experiment data from JSON and generate a readable TXT summary for documentation or archival use.

**Independent Test**: A researcher can import a valid JSON file with experiment records and generate a TXT report for one experiment without any remote services or model execution.

### Implementation for User Story 3

- [x] T017 [P] [US3] Implement JSON import parsing and schema validation in src/utils/json_import.py and src/app/storage.py, using the contract defined in contracts/experiment-import.schema.json
- [x] T018 [US3] Add import workflow actions and user feedback in src/app/main.py and src/app/ui/experiment_list.py
- [x] T019 [US3] Create the human-readable TXT report generator in src/app/report.py using the documented fields for id, name, date, model, dataset, configuration, hardware, reasoning_harness, observations, and recorded metrics
- [x] T020 [US3] Add report export action and file output handling in src/app/main.py and src/app/ui/detail_view.py

**Checkpoint**: At this point, the workflow supports import and reporting as independent research activities.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final hardening across all stories.

- [x] T021 [P] Review validation messages and ensure required-field errors are clear and consistent across form and import workflows in src/app/validation.py and src/app/ui/experiment_form.py
- [x] T022 [P] Run the regression checks for experiment creation, editing, deletion, import, and report generation using the scenarios in quickstart.md
- [x] T023 Document the local research workflow and final usage notes in docs/ or the project README for future maintainers
- [x] T024 Add the local Tkinter graphical interface and runnable `python -m src.app.main` entry point for the required create, list, view, edit, delete, import, report, and validation workflows

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; begins immediately.
- **Foundational (Phase 2)**: Depends on Setup completion and blocks all user story work.
- **User Story phases (Phases 3-5)**: Each depends on the Foundational phase and may proceed in priority order.
- **Polish (Phase 6)**: Depends on all desired user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational; no dependency on other stories.
- **User Story 2 (P1)**: Can start after Foundational; builds on the same experiment lifecycle.
- **User Story 3 (P2)**: Can start after Foundational; depends on the same registry model and does not require Story 1 or Story 2 completion to be independently testable.

### Parallel Opportunities

- T003 can run in parallel with T001 and T002.
- T005 and T006 can run in parallel once the models are defined in T004.
- T008 and T012 can run in parallel within User Story 1.
- T013 and T017 can run in parallel because they relate to different user flows but share the same underlying registry model.
- T021 and T022 can run in parallel during the final polish phase.

## Implementation Strategy

### MVP First

1. Complete Phase 1 and Phase 2.
2. Complete Phase 3: User Story 1.
3. Validate the create/list flow independently.
4. Add User Story 2 and User Story 3 as incremental value, keeping the infrastructure stable.

### Incremental Delivery

1. Setup + Foundation create the stable local registry and validation model.
2. Add registration and listing workflows.
3. Add editing and deletion.
4. Add import and TXT export.
5. Finish with cross-cutting polish and validation.

### Parallel Team Strategy

With multiple contributors:

1. One developer completes setup and foundational tasks.
2. Another developer works on User Story 1 while a second developer prepares the JSON import/report workflow.
3. Final validation and polish are done once all stories are integrated.
