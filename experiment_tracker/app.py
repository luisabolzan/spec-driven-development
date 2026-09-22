from __future__ import annotations

import json
import os
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Any

from .models import Experiment, generate_experiment_id, validate_experiment_data
from .storage import ExperimentStore


class ExperimentTrackerApp:
    def __init__(self, storage_path: str = "experiments.json", root: tk.Tk | None = None) -> None:
        self.root = root or tk.Tk()
        self.storage_path = Path(storage_path)
        self.store = ExperimentStore()
        self.selected_experiment_id: str | None = None
        self._build_ui()
        self.load_from_disk()
        self.refresh_experiment_list()

    @staticmethod
    def validate_experiment_payload(data: dict[str, Any]) -> list[str]:
        return validate_experiment_data(data)

    def _build_ui(self) -> None:
        self.root.title("Experiment Tracker")
        self.root.geometry("1100x720")
        self.root.minsize(980, 620)

        main = ttk.PanedWindow(self.root, orient="horizontal")
        main.pack(fill="both", expand=True, padx=10, pady=10)

        left = ttk.Frame(main, padding=(6, 6, 6, 6), width=320)
        main.add(left, weight=1)

        controls = ttk.Frame(left)
        controls.pack(fill="x", pady=(0, 8))

        ttk.Button(controls, text="New", command=self.new_experiment).pack(side="left", padx=(0, 6))
        ttk.Button(controls, text="Delete", command=self.delete_selected_experiment).pack(side="left", padx=(0, 6))
        ttk.Button(controls, text="Import JSON", command=self.import_experiments).pack(side="left", padx=(0, 6))
        ttk.Button(controls, text="Export JSON", command=self.export_experiments).pack(side="left")

        self.experiment_list = tk.Listbox(left, height=30, exportselection=False)
        self.experiment_list.pack(fill="both", expand=True)
        self.experiment_list.bind("<<ListboxSelect>>", self.on_experiment_selected)

        form_container = ttk.Frame(main, padding=(8, 6, 6, 6))
        main.add(form_container, weight=3)

        ttk.Label(form_container, text="Experiment Tracker", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 10))

        fields = ttk.Frame(form_container)
        fields.pack(fill="both", expand=True)

        self.field_vars: dict[str, tk.Variable] = {}
        self._add_form_row(fields, "Experiment ID", "experiment_id", disabled=True)
        self._add_form_row(fields, "Experiment Name", "name")
        self._add_form_row(fields, "Date (YYYY-MM-DD)", "date")
        self._add_form_row(fields, "Model", "model")
        self._add_form_row(fields, "Dataset", "dataset")
        self._add_form_row(fields, "Quantization / configuration", "configuration")
        self._add_form_row(fields, "CPU", "cpu")
        self._add_form_row(fields, "GPU", "gpu")
        self._add_form_row(fields, "Available RAM", "ram")

        row = ttk.Frame(fields)
        row.pack(fill="x", pady=4)
        ttk.Label(row, text="Reasoning harness used", width=22, anchor="w").pack(side="left")
        self.field_vars["reasoning_harness"] = tk.BooleanVar(value=False)
        ttk.Checkbutton(row, variable=self.field_vars["reasoning_harness"]).pack(side="left")

        self._add_form_row(fields, "Observation notes", "observations", multiline=True)

        metrics_frame = ttk.LabelFrame(fields, text="Evaluation Metrics")
        metrics_frame.pack(fill="x", pady=(10, 0))
        metrics_grid = ttk.Frame(metrics_frame, padding=(8, 8, 8, 8))
        metrics_grid.pack(fill="x")

        self._add_form_field(metrics_grid, "pass@1 (%)", "pass_at_1", 0)
        self._add_form_field(metrics_grid, "Execution time (s)", "execution_time_seconds", 1)
        self._add_form_field(metrics_grid, "Energy consumption (Wh)", "energy_consumption_wh", 2)

        button_row = ttk.Frame(form_container)
        button_row.pack(fill="x", pady=(12, 0))
        ttk.Button(button_row, text="Save Experiment", command=self.save_selected_experiment).pack(side="left", padx=(0, 8))
        ttk.Button(button_row, text="Generate TXT Report", command=self.generate_txt_report).pack(side="left")

    def _add_form_row(self, parent: ttk.Frame, label_text: str, key: str, multiline: bool = False, disabled: bool = False) -> None:
        row = ttk.Frame(parent)
        row.pack(fill="x", pady=4)
        label = ttk.Label(row, text=label_text, width=22, anchor="w")
        label.pack(side="left")

        if multiline:
            widget = tk.Text(row, height=5, width=60)
            widget.pack(side="left", fill="x", expand=True)
            self.field_vars[key] = widget
        else:
            widget = ttk.Entry(row)
            widget.pack(side="left", fill="x", expand=True)
            widget.configure(state="disabled" if disabled else "normal")
            self.field_vars[key] = widget

    def _add_form_field(self, parent: ttk.Frame, label_text: str, key: str, column: int) -> None:
        label = ttk.Label(parent, text=label_text)
        label.grid(row=0, column=column * 2, sticky="w", padx=(0, 8), pady=(0, 4))
        entry = ttk.Entry(parent, width=18)
        entry.grid(row=0, column=column * 2 + 1, sticky="w", padx=(0, 8), pady=(0, 4))
        self.field_vars[key] = entry

    def _set_field_value(self, key: str, value: Any) -> None:
        widget = self.field_vars[key]
        if isinstance(widget, tk.Text):
            widget.delete("1.0", tk.END)
            widget.insert("1.0", "" if value is None else str(value))
        elif isinstance(widget, tk.BooleanVar):
            widget.set(bool(value))
        else:
            widget.delete(0, tk.END)
            widget.insert(0, "" if value is None else str(value))

    def _get_field_value(self, key: str) -> Any:
        widget = self.field_vars[key]
        if isinstance(widget, tk.Text):
            return widget.get("1.0", tk.END).strip()
        if isinstance(widget, tk.BooleanVar):
            return widget.get()
        return widget.get().strip()

    def _set_form_for_experiment(self, experiment: Experiment | None) -> None:
        if experiment is None:
            self.selected_experiment_id = None
            for key in [
                "experiment_id",
                "name",
                "date",
                "model",
                "dataset",
                "configuration",
                "observations",
                "cpu",
                "gpu",
                "ram",
                "pass_at_1",
                "execution_time_seconds",
                "energy_consumption_wh",
            ]:
                self._set_field_value(key, "")
            self.field_vars["reasoning_harness"].set(False)
            self._set_field_value("experiment_id", self.store.next_experiment_id())
            return

        self.selected_experiment_id = experiment.experiment_id
        self._set_field_value("experiment_id", experiment.experiment_id)
        self._set_field_value("name", experiment.name)
        self._set_field_value("date", experiment.date)
        self._set_field_value("model", experiment.model)
        self._set_field_value("dataset", experiment.dataset)
        self._set_field_value("configuration", experiment.configuration)
        self._set_field_value("observations", experiment.observations)
        self._set_field_value("cpu", experiment.cpu)
        self._set_field_value("gpu", experiment.gpu)
        self._set_field_value("ram", experiment.ram)
        self.field_vars["reasoning_harness"].set(bool(experiment.reasoning_harness))
        self._set_field_value("pass_at_1", experiment.pass_at_1 if experiment.pass_at_1 is not None else "")
        self._set_field_value("execution_time_seconds", experiment.execution_time_seconds if experiment.execution_time_seconds is not None else "")
        self._set_field_value("energy_consumption_wh", experiment.energy_consumption_wh if experiment.energy_consumption_wh is not None else "")

    def refresh_experiment_list(self) -> None:
        self.experiment_list.delete(0, tk.END)
        for experiment in self.store.list_experiments():
            self.experiment_list.insert(tk.END, f"{experiment.experiment_id} - {experiment.name or 'Untitled experiment'}")

        if self.selected_experiment_id:
            for index in range(self.experiment_list.size()):
                item = self.experiment_list.get(index)
                if item.startswith(f"{self.selected_experiment_id} - "):
                    self.experiment_list.selection_set(index)
                    break
        else:
            self._set_form_for_experiment(None)

    def on_experiment_selected(self, event: Any) -> None:
        selection = self.experiment_list.curselection()
        if not selection:
            return
        experiment_id = self.experiment_list.get(selection[0]).split(" - ", 1)[0]
        experiment = self.store.get_experiment(experiment_id)
        if experiment:
            self._set_form_for_experiment(experiment)

    def new_experiment(self) -> None:
        self.selected_experiment_id = None
        self._set_form_for_experiment(None)
        self.experiment_list.selection_clear(0, tk.END)

    def save_selected_experiment(self) -> None:
        payload = {
            "experiment_id": self._get_field_value("experiment_id"),
            "name": self._get_field_value("name"),
            "date": self._get_field_value("date"),
            "model": self._get_field_value("model"),
            "dataset": self._get_field_value("dataset"),
            "configuration": self._get_field_value("configuration"),
            "observations": self._get_field_value("observations"),
            "cpu": self._get_field_value("cpu"),
            "gpu": self._get_field_value("gpu"),
            "ram": self._get_field_value("ram"),
            "reasoning_harness": self._get_field_value("reasoning_harness"),
            "pass_at_1": self._get_field_value("pass_at_1") or None,
            "execution_time_seconds": self._get_field_value("execution_time_seconds") or None,
            "energy_consumption_wh": self._get_field_value("energy_consumption_wh") or None,
        }

        errors = self.validate_experiment_payload(payload)
        if errors:
            messagebox.showerror("Validation error", "\n".join(errors))
            return

        experiment = Experiment.from_dict(payload)
        if self.selected_experiment_id and self.selected_experiment_id == experiment.experiment_id:
            self.store.upsert_experiment(experiment)
        elif self.selected_experiment_id and self.selected_experiment_id != experiment.experiment_id:
            self.store.delete_experiment(self.selected_experiment_id)
            self.store.add_experiment(experiment)
        elif not self.selected_experiment_id:
            if not experiment.experiment_id:
                experiment.experiment_id = self.store.next_experiment_id()
            self.store.add_experiment(experiment)

        self.selected_experiment_id = experiment.experiment_id
        self.save_to_disk()
        self.refresh_experiment_list()
        messagebox.showinfo("Experiment saved", f"Saved {experiment.experiment_id}.")

    def delete_selected_experiment(self) -> None:
        if not self.selected_experiment_id:
            messagebox.showwarning("No experiment selected", "Choose an experiment to delete.")
            return

        result = messagebox.askyesno("Delete experiment", f"Delete experiment {self.selected_experiment_id}?")
        if not result:
            return

        self.store.delete_experiment(self.selected_experiment_id)
        self.save_to_disk()
        self.selected_experiment_id = None
        self.refresh_experiment_list()
        self.new_experiment()

    def import_experiments(self) -> None:
        file_path = filedialog.askopenfilename(
            title="Import experiments from JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if not file_path:
            return

        try:
            imported = self.store.import_json(file_path)
            self.save_to_disk()
            self.refresh_experiment_list()
            self._set_form_for_experiment(imported[0] if imported else None)
            messagebox.showinfo("Import complete", f"Imported {len(imported)} experiment(s).")
        except Exception as exc:  # pragma: no cover - UI feedback path
            messagebox.showerror("Import failed", str(exc))

    def export_experiments(self) -> None:
        file_path = filedialog.asksaveasfilename(
            title="Export experiments as JSON",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
        )
        if not file_path:
            return
        try:
            self.store.export_json(file_path)
            messagebox.showinfo("Export complete", f"Saved {len(self.store.list_experiments())} experiment(s) to {file_path}.")
        except Exception as exc:  # pragma: no cover - UI feedback path
            messagebox.showerror("Export failed", str(exc))

    def generate_txt_report(self) -> None:
        if not self.selected_experiment_id:
            messagebox.showwarning("No experiment selected", "Select or save an experiment before generating a report.")
            return

        experiment = self.store.get_experiment(self.selected_experiment_id)
        if not experiment:
            messagebox.showwarning("Experiment not found", "The selected experiment could not be found.")
            return

        report = [
            f"Experiment: {experiment.name}",
            f"ID: {experiment.experiment_id}",
            f"Date: {experiment.date}",
            f"Model: {experiment.model}",
            f"Dataset: {experiment.dataset}",
            f"Configuration: {experiment.configuration}",
            f"CPU: {experiment.cpu}",
            f"GPU: {experiment.gpu}",
            f"RAM: {experiment.ram}",
            f"Reasoning harness: {'yes' if experiment.reasoning_harness else 'no'}",
            "",
            "Observation notes:",
            experiment.observations or "No observations recorded.",
            "",
            "Evaluation metrics:",
            f"pass@1: {experiment.pass_at_1 if experiment.pass_at_1 is not None else 'unavailable'}",
            f"Execution time (s): {experiment.execution_time_seconds if experiment.execution_time_seconds is not None else 'unavailable'}",
            f"Energy consumption (Wh): {experiment.energy_consumption_wh if experiment.energy_consumption_wh is not None else 'unavailable'}",
        ]

        file_path = filedialog.asksaveasfilename(
            title="Save TXT report",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
        )
        if not file_path:
            return

        Path(file_path).write_text("\n".join(report) + "\n", encoding="utf-8")
        messagebox.showinfo("Report generated", f"Saved report to {file_path}.")

    def load_from_disk(self) -> None:
        if not self.storage_path.exists():
            return
        try:
            payload = json.loads(self.storage_path.read_text(encoding="utf-8"))
            if isinstance(payload, list):
                self.store = ExperimentStore([Experiment.from_dict(item) for item in payload])
        except (json.JSONDecodeError, ValueError):
            self.store = ExperimentStore()

    def save_to_disk(self) -> None:
        os.makedirs(self.storage_path.parent, exist_ok=True)
        self.storage_path.write_text(self.store.to_json(), encoding="utf-8")

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    app = ExperimentTrackerApp()
    app.run()
