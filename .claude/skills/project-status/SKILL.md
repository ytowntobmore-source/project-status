---
name: project-status
user-invocable: true
description: "Capture, summarize, and recall your project status, blockers, milestones, and next actions."
---

# Project Status Skill

Use this skill when you want to keep track of a project status, generate a concise update, or remember where the project stands.

## When to use
- updating current project status
- summarizing progress for a standup or status report
- capturing blockers, risks, and next actions
- recalling project milestones and deadlines

## What it helps you remember
- project name and scope
- progress summary
- completed work and recent wins
- blockers and risks
- key milestones and due dates
- next actions and owners
- important context or assumptions

## How it works
- Add status updates to the workspace note file at `.claude/skills/project-status/status-notes.md`
- Use the skill to record new entries there or to summarize the latest project status
- Ask "Where am I on the project?" or "What is the current status?" and the skill will read the latest notes to answer

## How to use
1. Ask the skill to record or summarize the project status.
2. Provide the latest progress, blockers, dates, and next steps.
3. Use the output as a status note for meetings, updates, or your own reference.
4. Keep adding entries to `status-notes.md` so the skill can recall project history.

## Multi-project structure
Each project gets its own subfolder:
```
project-status/
  import_notes.py       ← shared script, handles all projects
  SKILL.md
  thousandeyes/
    status-notes.md
    imported/
  my-other-project/
    status-notes.md
    imported/
```
To add a new project, create a subfolder (e.g. `project-status/my-project/`) and drop `.txt` notes into it.

## Automatic imports from text files
- Drop `.txt` note files into the project's subfolder (e.g. `project-status/thousandeyes/my-note.txt`).
- Run `py import_notes.py` to import all projects, or `py import_notes.py <project-name>` for one project.
- Notes are appended to `<project>/status-notes.md` and the `.txt` is moved to `<project>/imported/`.

## Claude behavior — run import on every note mention
Whenever the user says they added notes, added a file, or asks about project status:
1. Check each project subfolder in `.claude/skills/project-status/` for any unimported `.txt` files.
2. If any are found, immediately run `py .claude/skills/project-status/import_notes.py` before answering.
3. Confirm what was imported, then provide the status summary.
4. Never ask the user to run the import manually — do it automatically.

## Example prompts
- "Record my current project status."
- "Summarize the project status for me."
- "What is the latest status, blockers, and next actions?"
- "Help me remember the current status of this project."
- "Add this to the project status notes in `status-notes.md`."
- "Where am I on the project based on the notes?"

## Status capture template
- Project: <project name>
- Scope: <what this covers>
- Progress: <brief summary>
- Completed: <recent achievements>
- Blockers: <current obstacles>
- Risks: <known or emerging risks>
- Next actions: <next steps>
- Due dates / milestones: <key dates>
- Notes: <any context or assumptions>
