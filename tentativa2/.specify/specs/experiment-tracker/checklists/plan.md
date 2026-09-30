# Planning Checklist

## Architecture
- [ ] Confirm local Python desktop app architecture and GUI toolkit choice
- [ ] Define app module layout with UI, domain, storage, and utilities separated cleanly
- [ ] Keep the solution lightweight and local, without remote dependencies

## Data Model and Persistence
- [ ] Define required fields: id, name, date, model
- [ ] Define optional fields and unspecified handling strategy
- [ ] Ensure missing values are stored consistently without placeholder invention
- [ ] Choose a local persistence format suitable for small desktop usage
- [ ] Define identifier generation and uniqueness rules

## UI and Navigation
- [ ] Create main list-detail layout with experiment list on one side and details on the other
- [ ] Use a single structured form for create and edit workflows
- [ ] Organize form into metadata, hardware, metrics, and notes sections
- [ ] Maintain a clean, minimal, modern, low-friction visual design
- [ ] Include filtering by model, dataset, and date

## Validation and Data Integrity
- [ ] Enforce minimal required-field validation
- [ ] Validate identifier uniqueness and malformed date or numeric data
- [ ] Avoid unnecessary restrictions on optional fields and missing values
- [ ] Provide actionable error messages for invalid input

## Incomplete Data Handling
- [ ] Support unspecified state for optional values and metrics
- [ ] Preserve partial experiment records without converting unknowns into fake values
- [ ] Display unspecified values clearly in the UI and reports

## Import and Export
- [ ] Accept valid JSON records that meet the minimum required fields
- [ ] Preserve missing optional fields as unspecified
- [ ] Reject malformed or incompatible records with clear feedback
- [ ] Generate clear human-readable TXT reports with unavailable data labeled appropriately

## Experiment Lifecycle
- [ ] Support create, view, edit, and delete workflows
- [ ] Add confirmation step for deletion
- [ ] Keep the first version focused on local research organization

## Testing
- [ ] Add tests for required-field enforcement
- [ ] Test import of valid partial records
- [ ] Test rejection of malformed or invalid records
- [ ] Test report generation with unspecified fields
- [ ] Test editing, filtering, and deletion flows
- [ ] Validate data integrity and user-facing messages
