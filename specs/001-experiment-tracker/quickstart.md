# Quickstart: Experiment Tracker

## Prerequisites

- Python 3.11 or later
- A local desktop environment capable of running a Python GUI application
- Access to project source code after implementation

## Local validation scenarios

### Launch the graphical application

From the repository root, run:

```powershell
.\.venv\Scripts\python.exe -m src.app.main
```

The application opens a local Tkinter window and stores records in `experiments.json`.

### 1. Create and save a valid experiment
1. Launch the application.
2. Select the option to create a new experiment.
3. Enter a unique ID, name, date, model, dataset, configuration, observations, and hardware details.
4. Set the reasoning harness flag.
5. Save the record.
6. Confirm the experiment appears in the list view.

Expected result: The record is persisted and visible in the registry.

### 2. Validate required field errors
1. Start a new experiment entry.
2. Leave a required field blank or provide invalid data.
3. Attempt to save.
4. Observe the validation message.

Expected result: The app blocks the save and explains which field is missing or invalid.

### 3. Edit an existing experiment
1. Select an experiment from the list.
2. Update one or more fields.
3. Save the change.

Expected result: The updated information is retained and visible in the details view.

### 4. Import JSON data
1. Prepare a valid JSON file with experiment records.
2. Choose the import action from the application menu.
3. Import the file.

Expected result: Each valid record is added to the registry; invalid records are rejected with clear feedback.

### 5. Generate a TXT report
1. Select an experiment from the list.
2. Choose the export or report action.
3. Review the generated TXT output.

Expected result: The output is human-readable and includes the experiment metadata and any recorded metrics.

## Validation commands

After implementation, the project should be validated with project-appropriate tests such as:

```bash
python -m pytest
```

This is intended as a quality gate for validation of experiment creation, storage, import, and report generation behaviors.
