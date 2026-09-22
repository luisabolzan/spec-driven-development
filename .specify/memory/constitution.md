<!--
Sync Impact Report
- Version change: 0.0.0 -> 1.0.0
- List of modified principles: initial constitution adopted from template scaffold
- Added sections: Core Principles, Project Constraints, Development Workflow, Governance
- Removed sections: none
- Follow-up TODOs: TODO(RATIFICATION_DATE): original adoption date was not recorded in the repository
-->

# spec-driven-development Constitution

## Core Principles

### I. Specification-First
The repository MUST treat requirements, design decisions, and acceptance conditions as first-class artifacts before implementation begins. Changes to behavior, interfaces, or workflows MUST be traceable to a specification, task, or explicit governance decision, and undocumented work is not considered approved.

This principle exists because ambiguity is the primary source of rework. By requiring a written definition of intent, the project reduces misalignment, preserves context across contributors, and makes reviewable decisions visible before code changes happen.

### II. Evidence Before Completion
Any substantive implementation claim MUST be backed by verifiable evidence: tests, lint or type checks, review artifacts, or direct execution results relevant to the changed behavior. A change is not complete until the evidence matches the intended outcome.

This keeps delivery grounded in reality rather than assumptions. The repository values demonstrable correctness over informal confidence, and it requires contributors to show the proof of their work in a traceable form.

### III. Test-First and Regression Safety
The project MUST prefer test-first validation for changed behavior, and every fix or feature MUST include coverage that would fail without the intended change. Regression tests are mandatory for bugs that recur or alter externally visible behavior.

This principle prevents unverified feature drift. By requiring tests to describe the target behavior before implementation, the project preserves correctness, lowers rework costs, and makes future refactors safer.

### IV. Small, Reviewable Changes
Work MUST be broken into the smallest logically complete units that can be reviewed, understood, and validated independently. Large or mixed-purpose changes are prohibited unless the scope is explicitly justified in the specification or PR description.

This principle reduces review risk and inspection overhead. Small increments allow faster feedback, simpler debugging, and clearer accountability for each decision in the project history.

### V. Clear Ownership and Documentation
Every artifact, decision, and dependency MUST have enough documentation and ownership to be understood by a future maintainer without hidden tribal knowledge. If a decision is intentional, it MUST be recorded in a stable artifact; if it is temporary, it MUST be marked as such.

This principle preserves continuity in a distributed and evolving project. Good documentation is not optional overhead; it is the mechanism that prevents architectural drift and keeps the repository maintainable over time.

## Project Constraints

The project MUST keep its governance, specification, and implementation artifacts aligned. The repository is not a place for informal decisions that are not recorded in the specification or constitution. Requirements and architecture decisions MUST be explicit, reviewable, and tied to the current branch or task context.

Implementation choices MUST remain consistent with the repository purpose as a spec-driven development workspace. Tools, scripts, and conventions MUST support the creation of auditable artifacts instead of creating hidden process steps. When trade-offs are made, the rationale MUST be explained in the relevant specification or documentation.

## Development Workflow

The workflow for this repository MUST follow this order:

1. Define the problem, scope, and expected behavior in a specification or task artifact.
2. Confirm the change is necessary, bounded, and traceable to a user or project need.
3. Implement the smallest valid unit of work with the supporting tests or validation steps.
4. Run the relevant checks and record the evidence.
5. Review the artifact, revise as needed, and only then mark the work complete.

All changes MUST be reviewable before merging. When a change introduces ambiguity, it MUST be clarified before implementation proceeds. The project MUST reject design-by-guessing and insist on explicit, testable definitions of success.

## Governance

This Constitution supersedes informal process preferences. Any repository practice that conflicts with this document MUST be treated as non-compliant until amended or explicitly justified in writing.

Amendments MUST be documented in this constitution, be reviewed for impact, and include a clear version bump and rationale. A proposal to change governance, a principle, or a required workflow MUST state the reason for the amendment, the affected sections, and the expected migration or compliance impact.

The project uses semantic versioning for governance updates:

- MAJOR: backward-incompatible governance removal or redefinition
- MINOR: new principle or materially expanded guidance
- PATCH: clarification, wording, or non-semantic refinement

Compliance review MUST verify that changes align with the stated principles and that evidence is present before implementation is treated as complete. Reviews must check for ambiguity, missing verification, and unrecorded decisions. Where a principle is not directly testable, the review must still require a clear, observable standard that can be checked by a future maintainer.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): original adoption date was not recorded in the repository | **Last Amended**: 2026-09-22
