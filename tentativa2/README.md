# Experiment Tracker

Experiment Tracker is a lightweight local desktop application for organizing research experiments involving language models, especially small models used for Python code generation.

## Features
- Create and manage experiments locally
- Auto-generate UUID experiment identifiers
- Store required metadata and optional research details
- Keep optional fields unspecified with null values when unavailable
- Filter experiments by model, dataset, and date
- Import experiment data from JSON
- Generate simple TXT reports
- Keep the first version focused on local research organization and reporting only

## Run locally

```bash
python main.py
```

## Requirements
- Python 3.10+
- Tkinter (included with standard Python distributions for most desktop installs)

## Notes
- This project is intentionally local and lightweight.
- It does not include remote services, authentication, model execution, or advanced analytics.
