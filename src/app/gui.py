from __future__ import annotations

import tkinter as tk
from datetime import date
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from src.utils.json_import import load_json_experiments

from .main import ExperimentTrackerApp
from .validation import ValidationError


def build_experiment_payload(field_values: dict[str, str], observations: str, reasoning_harness: bool) -> dict:
    metrics = {}
    for key in ("pass_at_1", "execution_time_seconds", "energy_consumption_wh"):
        value = field_values[key].strip()
        if value:
            try:
                metrics[key] = float(value)
            except ValueError as exc:
                raise ValidationError(f"{key} must be a number or blank.") from exc
        else:
            metrics[key] = None

    return {
        "id": field_values["id"],
        "name": field_values["name"],
        "date": field_values["date"],
        "model": field_values["model"],
        "dataset": field_values["dataset"],
        "configuration": field_values["configuration"],
        "observations": observations.strip(),
        "hardware": {
            "cpu": field_values["cpu"],
            "gpu": field_values["gpu"],
            "ram": field_values["ram"],
        },
        "reasoning_harness": reasoning_harness,
        "metrics": metrics,
    }


class ExperimentTrackerWindow:
    def __init__(self, root: tk.Tk, app: ExperimentTrackerApp):
        self.root = root
        self.app = app
        self.selected_id: str | None = None
        self.field_vars = {
            "id": tk.StringVar(),
            "name": tk.StringVar(),
            "date": tk.StringVar(value=date.today().isoformat()),
            "model": tk.StringVar(),
            "dataset": tk.StringVar(),
            "configuration": tk.StringVar(),
            "cpu": tk.StringVar(),
            "gpu": tk.StringVar(),
            "ram": tk.StringVar(),
            "pass_at_1": tk.StringVar(),
            "execution_time_seconds": tk.StringVar(),
            "energy_consumption_wh": tk.StringVar(),
        }
        self.reasoning_var = tk.BooleanVar(value=False)
        self.observations_text: tk.Text
        self.experiment_list: tk.Listbox
        self._build_window()
        self.refresh_list()

    def _build_window(self) -> None:
        self.root.title("Experiment Tracker")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)

        main = ttk.Frame(self.root, padding=12)
        main.pack(fill=tk.BOTH, expand=True)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(0, weight=1)

        list_frame = ttk.LabelFrame(main, text="Experiments", padding=8)
        list_frame.grid(row=0, column=0, sticky="ns", padx=(0, 12))
        list_frame.rowconfigure(0, weight=1)

        list_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.experiment_list = tk.Listbox(
            list_frame,
            width=30,
            exportselection=False,
            yscrollcommand=list_scroll.set,
        )
        list_scroll.configure(command=self.experiment_list.yview)
        self.experiment_list.grid(row=0, column=0, sticky="nsew")
        list_scroll.grid(row=0, column=1, sticky="ns")
        self.experiment_list.bind("<<ListboxSelect>>", self._select_experiment)

        list_actions = ttk.Frame(list_frame, padding=(0, 8, 0, 0))
        list_actions.grid(row=1, column=0, columnspan=2, sticky="ew")
        ttk.Button(list_actions, text="New", command=self.new_experiment).pack(fill=tk.X)
        ttk.Button(list_actions, text="Import JSON", command=self.import_json).pack(fill=tk.X, pady=(6, 0))
        ttk.Button(list_actions, text="Refresh", command=self.refresh_list).pack(fill=tk.X, pady=(6, 0))

        form_frame = ttk.LabelFrame(main, text="Experiment details", padding=12)
        form_frame.grid(row=0, column=1, sticky="nsew")
        form_frame.columnconfigure(1, weight=1)
        form_frame.rowconfigure(8, weight=1)

        fields = [
            ("ID", "id"),
            ("Name", "name"),
            ("Date (YYYY-MM-DD)", "date"),
            ("Model", "model"),
            ("Dataset", "dataset"),
            ("Configuration", "configuration"),
            ("CPU", "cpu"),
            ("GPU", "gpu"),
            ("RAM", "ram"),
            ("Pass@1", "pass_at_1"),
            ("Execution time (seconds)", "execution_time_seconds"),
            ("Energy consumption (Wh)", "energy_consumption_wh"),
        ]
        for row, (label, key) in enumerate(fields):
            ttk.Label(form_frame, text=label).grid(row=row, column=0, sticky="w", padx=(0, 10), pady=3)
            ttk.Entry(form_frame, textvariable=self.field_vars[key]).grid(
                row=row, column=1, sticky="ew", pady=3
            )

        ttk.Checkbutton(
            form_frame,
            text="Reasoning-oriented harness used",
            variable=self.reasoning_var,
        ).grid(row=len(fields), column=0, columnspan=2, sticky="w", pady=(8, 3))

        ttk.Label(form_frame, text="Observations").grid(
            row=len(fields) + 1, column=0, sticky="nw", padx=(0, 10), pady=3
        )
        self.observations_text = tk.Text(form_frame, height=6, width=50, wrap=tk.WORD)
        self.observations_text.grid(row=len(fields) + 1, column=1, sticky="nsew", pady=3)

        actions = ttk.Frame(form_frame, padding=(0, 12, 0, 0))
        actions.grid(row=len(fields) + 2, column=0, columnspan=2, sticky="ew")
        ttk.Button(actions, text="Save", command=self.save_experiment).pack(side=tk.LEFT)
        ttk.Button(actions, text="Delete", command=self.delete_experiment).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(actions, text="Export TXT report", command=self.export_report).pack(side=tk.LEFT, padx=(8, 0))

    def refresh_list(self) -> None:
        try:
            experiments = self.app.store.list_experiments()
        except (OSError, ValueError, ValidationError) as exc:
            self._show_error("Unable to load experiments", exc)
            return

        self.app.list_experiments()
        self.experiment_list.delete(0, tk.END)
        for experiment in experiments:
            self.experiment_list.insert(tk.END, f"{experiment.id} - {experiment.name}")

    def _select_experiment(self, _event: tk.Event) -> None:
        selection = self.experiment_list.curselection()
        if not selection:
            return
        experiments = self.app.store.list_experiments()
        if selection[0] >= len(experiments):
            return
        self._load_experiment(experiments[selection[0]])

    def _load_experiment(self, experiment) -> None:
        data = experiment.to_dict()
        self.selected_id = experiment.id
        hardware = data["hardware"]
        metrics = data.get("metrics") or {}
        values = {
            "id": data["id"],
            "name": data["name"],
            "date": data["date"],
            "model": data["model"],
            "dataset": data["dataset"],
            "configuration": data["configuration"],
            "cpu": hardware["cpu"],
            "gpu": hardware["gpu"],
            "ram": hardware["ram"],
            "pass_at_1": metrics.get("pass_at_1", ""),
            "execution_time_seconds": metrics.get("execution_time_seconds", ""),
            "energy_consumption_wh": metrics.get("energy_consumption_wh", ""),
        }
        for key, value in values.items():
            self.field_vars[key].set("" if value is None else str(value))
        self.reasoning_var.set(data["reasoning_harness"])
        self.observations_text.delete("1.0", tk.END)
        self.observations_text.insert("1.0", data["observations"])

    def new_experiment(self) -> None:
        self.selected_id = None
        for variable in self.field_vars.values():
            variable.set("")
        self.field_vars["date"].set(date.today().isoformat())
        self.reasoning_var.set(False)
        self.observations_text.delete("1.0", tk.END)
        self.experiment_list.selection_clear(0, tk.END)

    def _form_payload(self) -> dict:
        field_values = {key: variable.get() for key, variable in self.field_vars.items()}
        observations = self.observations_text.get("1.0", tk.END)
        return build_experiment_payload(field_values, observations, self.reasoning_var.get())

    def save_experiment(self) -> None:
        try:
            payload = self._form_payload()
            if self.selected_id is None:
                experiment = self.app.save_experiment(payload)
            else:
                experiment = self.app.update_experiment(payload)
            self.selected_id = experiment.id
            self.refresh_list()
            self._show_info("Saved", f"Experiment '{experiment.id}' was saved.")
        except (ValidationError, OSError) as exc:
            self._show_error("Could not save experiment", exc)

    def delete_experiment(self) -> None:
        if self.selected_id is None:
            self._show_error("Delete experiment", "Select an experiment first.")
            return
        if not messagebox.askyesno("Delete experiment", f"Delete '{self.selected_id}'?"):
            return
        try:
            self.app.delete_experiment(self.selected_id)
            self.new_experiment()
            self.refresh_list()
        except (ValidationError, OSError) as exc:
            self._show_error("Could not delete experiment", exc)

    def import_json(self) -> None:
        path = filedialog.askopenfilename(
            title="Import experiments",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            experiments = load_json_experiments(path)
            imported = self.app.import_experiments({"experiments": experiments})
            self.refresh_list()
            self._show_info("Import complete", f"Imported {len(imported)} experiment(s).")
        except (OSError, ValueError, ValidationError) as exc:
            self._show_error("Could not import experiments", exc)

    def export_report(self) -> None:
        if self.selected_id is None:
            self._show_error("Export report", "Select an experiment first.")
            return
        path = filedialog.asksaveasfilename(
            title="Save TXT report",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"{self.selected_id}.txt",
        )
        if not path:
            return
        try:
            Path(path).write_text(self.app.export_report(self.selected_id), encoding="utf-8")
            self._show_info("Report exported", f"Saved report to {path}.")
        except (OSError, ValidationError) as exc:
            self._show_error("Could not export report", exc)

    def _show_info(self, title: str, message: str) -> None:
        messagebox.showinfo(title, message, parent=self.root)

    def _show_error(self, title: str, error: Exception | str) -> None:
        messagebox.showerror(title, str(error), parent=self.root)


def run_gui(storage_path: str | Path = "experiments.json") -> None:
    root = tk.Tk()
    app = ExperimentTrackerApp(storage_path)
    ExperimentTrackerWindow(root, app)
    root.mainloop()
