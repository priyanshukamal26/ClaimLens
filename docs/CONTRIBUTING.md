# CONTRIBUTING.md — AI Agent & Developer Guide

Welcome to the ClaimLens Nexus project. Whether you are a human developer or an AI Coding Agent, this guide dictates how you interact with the codebase.

## The Universal Rule

**Before modifying ANY code, you must read `docs/MASTER.md`.**

The `docs/` folder is the single source of truth for the project's state. It contains the architecture, the decisions (ADRs), the UI/UX design system, and the current task list. If you do not read the documentation, you will break the system.

## AI Agent Handoff Protocol

Because this project is built across multiple sessions by different AI agents, we enforce a strict state-preservation protocol.

If you are an AI agent finishing a session, you MUST:
1. Ensure the code compiles and runs locally (run `pytest tests/test_guard.py` and `npx vite build`).
2. Update `docs/HISTORY.md` with a summary of the exact work you accomplished, files touched, and architectural decisions made.
3. Update `docs/PROJECT_TRACK.md` to reflect the new state of the project.
4. Update `docs/NEXT_SESSION.md` with a specific, ready-to-copy prompt for the *next* agent, detailing exactly what they need to do next and what blockers exist.

## Code Style & Guidelines

### Backend (Python)
- Use standard Python typing (e.g., `Optional[str]`).
- All FastAPI endpoints must have a descriptive docstring.
- Database access must use the context managers defined in `app/database.py`.
- **Never** bypass the `sqlglot` guard in `app/agent/guard.py`.

### Frontend (React)
- Use functional components and hooks.
- **Do not introduce Tailwind CSS**. We are using a custom CSS variable system defined in `index.css` to maintain absolute control over the design system.
- Follow the visual language defined in `UI_UX_DESIGN_SYSTEM.md`.

## Pull Requests
- All PRs must pass the CI/CD pipeline (`.github/workflows/ci.yml`), which includes the 25-case hostile SQL test suite.
