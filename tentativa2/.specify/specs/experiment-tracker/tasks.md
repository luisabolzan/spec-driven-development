# Tasks: Experiment Tracker

## 1. Project Setup
- [ ] Initialize a local Python desktop project structure for the Experiment Tracker app.
- [ ] Choose and configure the v1 Tkinter-based GUI project layout.
- [ ] Define the local app folder and storage location for experiment data.
- [ ] Create the initial package/module layout for UI, domain logic, persistence, and utilities.

## 2. Core Domain Model
- [ ] Define the Experiment data model with required and optional fields.
- [ ] Add support for UUID-based automatic identifier generation.
- [ ] Persist unspecified optional values as null in the stored JSON data model.
- [ ] Do not use placeholder values such as "N/A" or 0 unless explicitly entered by the user.
- [ ] Define minimal validation rules for required fields and data integrity.
- [ ] Define clear serialization rules for JSON persistence.
- [ ] Keep the UI free to display user-friendly labels such as "Not specified" or "Not available" when values are unset.

## 3. Local Persistence
- [ ] Implement local JSON storage for experiment records.
- [ ] Add save behavior for new experiments.
- [ ] Add load behavior for stored experiments.
- [ ] Add update behavior for edited experiments.
- [ ] Add delete behavior for permanent removal.
- [ ] Ensure records remain valid even when optional data is missing.

## 4. Main GUI Layout
- [ ] Build the main application window with a list pane and detail pane.
- [ ] Add a primary action for creating a new experiment.
- [ ] Add controls for filtering by model, dataset, and date.
- [ ] Add actions for viewing details, editing, deleting, importing, and generating a report.
- [ ] Apply consistent visual styling, spacing, typography, section hierarchy, and interactive states across the main window, forms, lists, dialogs, and detail views.
- [ ] Keep the visual design clean, modern, intuitive, and polished without unnecessary decoration.
- [ ] Provide a clear and friendly empty state when no experiments are registered, including an obvious action for creating the first experiment.
- [ ] Keep Tkinter as the GUI framework for v1.

## 5. Experiment Form Workflow
- [ ] Implement a single structured form for creating and editing experiments.
- [ ] Organize the form into metadata, hardware, metrics, and notes sections.
- [ ] Populate the form with existing values when editing.
- [ ] Validate required fields on save.
- [ ] Preserve all values already entered by the user when validation fails and clearly indicate the fields requiring correction.
- [ ] Support optional fields left blank or unspecified without injecting placeholder values.
- [ ] Keep UUID-based automatic identifier generation; the user should not manually enter the experiment identifier.

## 6. Experiment Browsing and Details
- [ ] Display a compact experiment list with key summary fields.
- [ ] Allow selecting an experiment to view its full details.
- [ ] Show metadata, hardware, metrics, and notes in a clear structure.
- [ ] Maintain a low-friction workflow for navigating between list, detail, and edit modes.

## 7. JSON Import
- [ ] Implement JSON import for experiment records.
- [ ] Accept records that satisfy the minimum required fields.
- [ ] Preserve missing optional data as unspecified instead of inventing values.
- [ ] Validate malformed or incompatible records with clear user feedback.
- [ ] Report import outcomes, including skipped or invalid records.

## 8. TXT Reporting
- [ ] Implement generation of a human-readable TXT report.
- [ ] Include available experiment sections and details in a clear layout.
- [ ] Label missing or unavailable values as unspecified/not available.
- [ ] Ensure the report remains readable even when some metrics or information are missing.

## 9. Validation and User Feedback
- [ ] Show actionable validation messages for invalid input.
- [ ] Highlight the fields that require correction when a form fails validation.
- [ ] Keep validation focused on required fields and data integrity rather than unnecessary restrictions.
- [ ] Confirm destructive actions with a clear deletion prompt.

## 10. Automated Testing
- [ ] Add tests for required-field enforcement.
- [ ] Add tests for automatic UUID generation and uniqueness.
- [ ] Add tests for saving and loading experiments with missing optional data.
- [ ] Add tests for editing and deleting experiments.
- [ ] Add tests for filtering by model, dataset, and date.
- [ ] Add tests for JSON import with valid partial records and invalid records.
- [ ] Add tests for TXT report generation when information is missing.
- [ ] Add tests for validation feedback and preserved form values on failure.

## 11. Final Verification
- [ ] Verify the app remains local and lightweight.
- [ ] Verify no remote services, authentication, or model execution are included.
- [ ] Verify the product stays aligned with the clarified requirements and scope.
