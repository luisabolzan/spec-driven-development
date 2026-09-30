from __future__ import annotations

import uuid
from pathlib import Path
from tkinter import BooleanVar, StringVar, Tk, Toplevel, ttk, messagebox, filedialog
from tkinter import LEFT, BOTH, RIGHT, W, END, N, E, S

from .models import Experiment, validate_experiment, format_display_value
from .report import generate_txt_report
from .storage import ExperimentStore


class ExperimentFormDialog(Toplevel):
    def __init__(self, parent: "ExperimentTrackerApp", experiment: Experiment | None = None):
        super().__init__(parent)
        self.parent = parent
        self.experiment = experiment
        self.title("Edit experiment" if experiment else "New experiment")
        self.geometry("760x680")
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()

        self.field_widgets: dict[str, object] = {}
        self.error_fields: set[str] = set()

        main = ttk.Frame(self, padding=12)
        main.pack(fill="both", expand=True)

        self.notebook = ttk.Notebook(main)
        self.notebook.pack(fill="both", expand=True)

        metadata = ttk.Frame(self.notebook, padding=12)
        hardware = ttk.Frame(self.notebook, padding=12)
        metrics = ttk.Frame(self.notebook, padding=12)
        notes = ttk.Frame(self.notebook, padding=12)

        self.notebook.add(metadata, text="Metadata")
        self.notebook.add(hardware, text="Hardware")
        self.notebook.add(metrics, text="Metrics")
        self.notebook.add(notes, text="Notes")

        self._add_fields(metadata, [
            ("name", "Name", True),
            ("date", "Date (YYYY-MM-DD)", True),
            ("model", "Model", True),
            ("dataset", "Dataset", False),
            ("quantization_config", "Quantization / Configuration", False),
        ])

        self._add_fields(hardware, [
            ("hardware_cpu", "CPU", False),
            ("hardware_gpu", "GPU", False),
            ("hardware_ram", "RAM", False),
        ])

        self._add_fields(metrics, [
            ("pass_at_1", "pass@1", False),
            ("execution_time", "Execution Time", False),
            ("energy_consumption", "Energy Consumption", False),
            ("reasoning_harness_used", "Reasoning Harness Used", False, "bool"),
        ])

        self._add_fields(notes, [
            ("notes", "Notes / Observations", False, "textarea"),
        ])

        button_bar = ttk.Frame(main)
        button_bar.pack(fill="x", pady=(12, 0))
        ttk.Button(button_bar, text="Save", command=self.save).pack(side=RIGHT, padx=(0, 6))
        ttk.Button(button_bar, text="Cancel", command=self.destroy).pack(side=RIGHT)

        if experiment:
            self.populate(experiment)
        else:
            self._set_field_value("id", str(uuid.uuid4()))

    def _add_fields(self, parent, rows):
        for row in rows:
            key, label, required, field_type = (row[0], row[1], row[2], row[3] if len(row) > 3 else "text")
            label_widget = ttk.Label(parent, text=label + (" *" if required else ""))
            label_widget.grid(row=len(parent.grid_slaves()) + 1, column=0, sticky=W, padx=(0, 8), pady=6)

            widget = None
            if field_type == "textarea":
                widget = tk_text = __import__('tkinter').Text(parent, height=7, width=70, wrap="word")
                widget.grid(row=len(parent.grid_slaves()) + 1, column=1, sticky="nsew", padx=6, pady=6)
                parent.grid_columnconfigure(1, weight=1)
            elif field_type == "bool":
                widget = ttk.Combobox(parent, values=["", "Yes", "No"], state="readonly", width=30)
                widget.grid(row=len(parent.grid_slaves()) + 1, column=1, sticky=W, padx=6, pady=6)
            else:
                widget = ttk.Entry(parent, width=50)
                widget.grid(row=len(parent.grid_slaves()) + 1, column=1, sticky="ew", padx=6, pady=6)
                parent.grid_columnconfigure(1, weight=1)

            self.field_widgets[key] = widget

    def _set_field_value(self, key: str, value: object) -> None:
        widget = self.field_widgets.get(key)
        if widget is None:
            return
        if isinstance(widget, ttk.Combobox):
            if value is None:
                widget.set("")
            elif value is True:
                widget.set("Yes")
            elif value is False:
                widget.set("No")
            else:
                widget.set(str(value))
        elif hasattr(widget, "delete") and hasattr(widget, "insert"):
            widget.delete(0, END)
            widget.insert(0, "" if value is None else str(value))
        elif hasattr(widget, "delete") and hasattr(widget, "insert") and hasattr(widget, "get"):
            widget.delete("1.0", END)
            widget.insert("1.0", "" if value is None else str(value))
        else:
            if hasattr(widget, "delete"):
                widget.delete(0, END)
                widget.insert(0, "" if value is None else str(value))

    def populate(self, experiment: Experiment) -> None:
        for key in [
            "id", "name", "date", "model", "dataset", "quantization_config",
            "hardware_cpu", "hardware_gpu", "hardware_ram",
            "pass_at_1", "execution_time", "energy_consumption",
            "reasoning_harness_used", "notes"
        ]:
            value = getattr(experiment, key)
            self._set_field_value(key, value)

    def _validate_and_collect(self) -> tuple[Experiment | None, dict[str, str]]:
        data: dict[str, object] = {}
        for key, widget in self.field_widgets.items():
            if key == "id":
                data[key] = self.experiment.id if self.experiment else (widget.get().strip() or str(uuid.uuid4()))
                continue
            if isinstance(widget, ttk.Combobox):
                raw = widget.get().strip()
                if raw in ("", "Not specified"):
                    data[key] = None
                elif raw == "Yes":
                    data[key] = True
                elif raw == "No":
                    data[key] = False
                else:
                    data[key] = raw or None
            elif hasattr(widget, "get") and hasattr(widget, "winfo_class") and widget.winfo_class() == "TEntry":
                text = widget.get().strip()
                data[key] = None if text == "" else text
            elif hasattr(widget, "get") and hasattr(widget, "winfo_class") and widget.winfo_class() == "Text":
                text = widget.get("1.0", END).strip()
                data[key] = None if text == "" else text
            else:
                data[key] = None

        if self.experiment is not None:
            data["id"] = self.experiment.id
        else:
            data["id"] = str(uuid.uuid4())

        experiment = Experiment.from_dict(data)
        errors = validate_experiment(experiment)
        return experiment, errors

    def save(self) -> None:
        experiment, errors = self._validate_and_collect()
        if not experiment or errors:
            self._highlight_errors(errors)
            messagebox.showerror("Validation error", "Please correct the highlighted fields before saving.")
            return

        self.parent.save_experiment(experiment)
        self.destroy()

    def _highlight_errors(self, errors: dict[str, str]) -> None:
        for key in self.field_widgets:
            widget = self.field_widgets[key]
            if key in errors:
                if isinstance(widget, ttk.Combobox):
                    widget.configure(foreground="red", background="#fff0f0")
                elif hasattr(widget, "configure"):
                    widget.configure(background="#fff0f0")
            else:
                if isinstance(widget, ttk.Combobox):
                    widget.configure(foreground="black", background="white")
                elif hasattr(widget, "configure"):
                    widget.configure(background="white")


class ExperimentTrackerApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Experiment Tracker")
        self.geometry("1100x700")
        self.minsize(900, 560)

        self.store = ExperimentStore()
        self.experiments = self.store.load()
        self.filter_model = StringVar()
        self.filter_dataset = StringVar()
        self.filter_date = StringVar()

        self._build_ui()
        self.refresh_list()

    def _build_ui(self):
        self.configure(background="#f3f4f6")

        top = ttk.Frame(self, padding=(12, 12, 12, 8))
        top.pack(fill="x")

        title = ttk.Label(top, text="Experiment Tracker", font=("Segoe UI", 16, "bold"))
        title.pack(anchor=W)

        actions = ttk.Frame(top)
        actions.pack(fill="x", pady=(10, 0))

        ttk.Button(actions, text="New Experiment", command=self.new_experiment).pack(side=LEFT, padx=(0, 8))
        ttk.Button(actions, text="Edit", command=self.edit_selected_experiment).pack(side=LEFT, padx=(0, 8))
        ttk.Button(actions, text="Delete", command=self.delete_selected_experiment).pack(side=LEFT, padx=(0, 8))
        ttk.Button(actions, text="Import JSON", command=self.import_json).pack(side=LEFT, padx=(0, 8))
        ttk.Button(actions, text="Generate TXT Report", command=self.generate_report).pack(side=LEFT)

        filter_bar = ttk.Frame(self)
        filter_bar.pack(fill="x", padx=12, pady=(0, 10))
        ttk.Label(filter_bar, text="Model").grid(row=0, column=0, sticky=W, padx=(0, 6))
        ttk.Entry(filter_bar, textvariable=self.filter_model, width=20).grid(row=0, column=1, padx=(0, 12))
        ttk.Label(filter_bar, text="Dataset").grid(row=0, column=2, sticky=W, padx=(0, 6))
        ttk.Entry(filter_bar, textvariable=self.filter_dataset, width=20).grid(row=0, column=3, padx=(0, 12))
        ttk.Label(filter_bar, text="Date").grid(row=0, column=4, sticky=W, padx=(0, 6))
        ttk.Entry(filter_bar, textvariable=self.filter_date, width=18).grid(row=0, column=5, padx=(0, 12))
        ttk.Button(filter_bar, text="Apply Filters", command=self.refresh_list).grid(row=0, column=6)

        main = ttk.Frame(self)
        main.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.list_panel = ttk.Frame(main, padding=8)
        self.list_panel.pack(side=LEFT, fill="y", padx=(0, 10))
        self.listbox = tk_listbox = __import__('tkinter').Listbox(self.list_panel, width=48, height=30, exportselection=False)
        self.listbox.pack(side=LEFT, fill="both", expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.on_list_select)

        self.scrollbar = ttk.Scrollbar(self.list_panel, orient="vertical", command=self.listbox.yview)
        self.scrollbar.pack(side=RIGHT, fill="y")
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.detail_panel = ttk.Frame(main, padding=8)
        self.detail_panel.pack(side=LEFT, fill="both", expand=True)
        self.detail_text = __import__('tkinter').Text(self.detail_panel, wrap="word", state="disabled", font=("Segoe UI", 10))
        self.detail_text.pack(fill="both", expand=True)

        self.empty_state = ttk.Frame(self, padding=20)
        self.empty_state.pack(fill="both", expand=True)
        self.empty_label = ttk.Label(self.empty_state, text="No experiments registered yet.", font=("Segoe UI", 12))
        self.empty_label.pack(pady=(0, 8))
        self.empty_button = ttk.Button(self.empty_state, text="Create the first experiment", command=self.new_experiment)
        self.empty_button.pack()
        self.empty_state.pack_forget()

    def _filtered_experiments(self) -> list[Experiment]:
        model_filter = self.filter_model.get().strip().lower()
        dataset_filter = self.filter_dataset.get().strip().lower()
        date_filter = self.filter_date.get().strip().lower()

        filtered = []
        for experiment in self.experiments:
            if model_filter and model_filter not in (experiment.model or "").lower():
                continue
            if dataset_filter and dataset_filter not in (experiment.dataset or "").lower():
                continue
            if date_filter and date_filter not in (experiment.date or "").lower():
                continue
            filtered.append(experiment)
        return filtered

    def refresh_list(self):
        filtered = self._filtered_experiments()
        self.listbox.delete(0, END)
        for experiment in filtered:
            label = f"{experiment.date} | {experiment.model} | {experiment.name}"
            self.listbox.insert(END, label)

        if not filtered:
            self.list_panel.pack_forget()
            self.detail_panel.pack_forget()
            self.empty_state.pack(fill="both", expand=True, padx=12, pady=(0, 12))
            self.detail_text.configure(state="normal")
            self.detail_text.delete("1.0", END)
            self.detail_text.insert("1.0", "Select a record or create a new experiment.")
            self.detail_text.configure(state="disabled")
            return

        self.empty_state.pack_forget()
        self.list_panel.pack(side=LEFT, fill="y", padx=(0, 10))
        self.detail_panel.pack(side=LEFT, fill="both", expand=True)

        if self.listbox.size() > 0:
            self.listbox.selection_set(0)
            self.on_list_select(None)

    def on_list_select(self, _event):
        index = self.listbox.curselection()
        if not index:
            return
        selection = self._filtered_experiments()[index[0]]
        self._render_detail(selection)

    def _render_detail(self, experiment: Experiment) -> None:
        lines = [
            f"ID: {experiment.id}",
            f"Name: {experiment.name}",
            f"Date: {experiment.date}",
            f"Model: {experiment.model}",
            f"Dataset: {format_display_value(experiment.dataset)}",
            f"Quantization / Configuration: {format_display_value(experiment.quantization_config)}",
            f"CPU: {format_display_value(experiment.hardware_cpu)}",
            f"GPU: {format_display_value(experiment.hardware_gpu)}",
            f"RAM: {format_display_value(experiment.hardware_ram)}",
            f"Reasoning Harness Used: {format_display_value(experiment.reasoning_harness_used)}",
            f"pass@1: {format_display_value(experiment.pass_at_1)}",
            f"Execution Time: {format_display_value(experiment.execution_time)}",
            f"Energy Consumption: {format_display_value(experiment.energy_consumption)}",
            f"Notes: {format_display_value(experiment.notes)}",
        ]
        self.detail_text.configure(state="normal")
        self.detail_text.delete("1.0", END)
        self.detail_text.insert("1.0", "\n".join(lines))
        self.detail_text.configure(state="disabled")

    def new_experiment(self):
        ExperimentFormDialog(self, None)

    def edit_selected_experiment(self):
        selection = self._selected_experiment_from_list()
        if selection is None:
            messagebox.showinfo("No selection", "Please select an experiment to edit.")
            return
        ExperimentFormDialog(self, selection)

    def _selected_experiment_from_list(self) -> Experiment | None:
        index = self.listbox.curselection()
        if not index:
            return None
        filtered = self._filtered_experiments()
        if index[0] >= len(filtered):
            return None
        return filtered[index[0]]

    def save_experiment(self, experiment: Experiment) -> None:
        existing = self.experiments
        if any(item.id == experiment.id for item in existing):
            self.experiments = [item if item.id != experiment.id else experiment for item in existing]
        else:
            self.experiments.append(experiment)
        self.store.save(self.experiments)
        self.refresh_list()

    def delete_selected_experiment(self):
        selection = self._selected_experiment_from_list()
        if selection is None:
            messagebox.showinfo("No selection", "Please select an experiment to delete.")
            return
        confirm = messagebox.askyesno("Delete experiment", f"Delete experiment '{selection.name}'?")
        if not confirm:
            return
        self.experiments = [item for item in self.experiments if item.id != selection.id]
        self.store.save(self.experiments)
        self.refresh_list()

    def import_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not file_path:
            return
        imported, errors = self.store.import_from_json(file_path)
        if errors:
            messagebox.showwarning("Import warnings", "\n".join(errors))
        if imported:
            existing_ids = {item.id for item in self.experiments}
            for experiment in imported:
                if experiment.id not in existing_ids:
                    self.experiments.append(experiment)
                    existing_ids.add(experiment.id)
            self.store.save(self.experiments)
            self.refresh_list()
            messagebox.showinfo("Import complete", f"Imported {len(imported)} experiment(s).")

    def generate_report(self):
        if not self.experiments:
            messagebox.showinfo("No experiments", "There are no experiments to report yet.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not file_path:
            return
        report = generate_txt_report(self.experiments)
        Path(file_path).write_text(report, encoding="utf-8")
        messagebox.showinfo("Report generated", f"TXT report saved to {file_path}")
