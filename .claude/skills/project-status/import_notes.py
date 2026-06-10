from __future__ import annotations

import argparse
import datetime
from pathlib import Path
import re

PROJECT_STATUS_DIR = Path(__file__).parent
DUE_DATE_REGEX = re.compile(r"(?:due|deadline|by|milestone)[:\s]+(\d{1,2}/\d{1,2}(?:/\d{2,4})?)", re.IGNORECASE)
PROJECT_LINE_DATE_REGEX = re.compile(r"^(.+?)\s+(\d{1,2}/\d{1,2}(?:/\d{2,4})?)$")


def parse_note_text(text: str, filename: str) -> tuple[str, str, str, str, str, str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return filename, "", "None recorded", "None recorded", "None recorded", "Imported note file."

    first_line = lines[0]
    match = PROJECT_LINE_DATE_REGEX.match(first_line)
    project = match.group(1).strip() if match else first_line
    summary = " ".join(lines)

    due_date = "None recorded"
    date_match = DUE_DATE_REGEX.search(text)
    if date_match:
        due_date = date_match.group(1)

    return project, summary, due_date, "None recorded", "None recorded", "Imported note file."


def build_entry(filename: str, content: str) -> str:
    project, summary, due_date, blockers, risks, notes = parse_note_text(content, filename)
    date = datetime.date.today().isoformat()
    return (
        f"## Imported note: {filename}\n\n"
        f"- Date: {date}\n"
        f"- Project: {project}\n"
        f"- Scope: Imported note file\n"
        f"- Progress: {summary}\n"
        f"- Completed: None recorded\n"
        f"- Blockers: {blockers}\n"
        f"- Risks: {risks}\n"
        f"- Next actions: Review the imported note and update as needed\n"
        f"- Due dates / milestones: {due_date}\n"
        f"- Notes: {notes}\n\n"
    )


def already_imported(status_text: str, filename: str) -> bool:
    return f"## Imported note: {filename}" in status_text


def import_project(project_dir: Path) -> int:
    import_dir = project_dir / "imported"
    status_file = project_dir / "status-notes.md"

    import_dir.mkdir(exist_ok=True)

    if not status_file.exists():
        status_file.write_text(f"# {project_dir.name} Status Notes\n\n", encoding="utf-8")

    status_text = status_file.read_text(encoding="utf-8")
    txt_files = sorted(project_dir.glob("*.txt"))

    entries = []
    for txt_file in txt_files:
        if already_imported(status_text, txt_file.stem):
            destination = import_dir / txt_file.name
            if not destination.exists():
                txt_file.replace(destination)
            print(f"  Skipping already imported: {txt_file.name}")
            continue

        content = txt_file.read_text(encoding="utf-8").strip()
        if not content:
            print(f"  Skipping empty file: {txt_file.name}")
            continue

        entries.append(build_entry(txt_file.stem, content))
        destination = import_dir / txt_file.name
        txt_file.replace(destination)
        print(f"  Imported: {txt_file.name}")

    if entries:
        with status_file.open("a", encoding="utf-8") as f:
            f.write("\n".join(entries))
        print(f"  Appended {len(entries)} entr{'y' if len(entries) == 1 else 'ies'} to {project_dir.name}/status-notes.md")

    return len(entries)


def main() -> int:
    parser = argparse.ArgumentParser(description="Import .txt notes into project status files.")
    parser.add_argument("project", nargs="?", help="Project subfolder name (default: all projects)")
    args = parser.parse_args()

    if args.project:
        project_dir = PROJECT_STATUS_DIR / args.project
        if not project_dir.is_dir():
            print(f"Project folder not found: {project_dir}")
            return 1
        project_dirs = [project_dir]
    else:
        project_dirs = [
            d for d in sorted(PROJECT_STATUS_DIR.iterdir())
            if d.is_dir() and not d.name.startswith(".")
        ]

    if not project_dirs:
        print("No project folders found.")
        return 0

    total = 0
    for project_dir in project_dirs:
        txt_files = list(project_dir.glob("*.txt"))
        if txt_files or (project_dir / "status-notes.md").exists():
            print(f"[{project_dir.name}]")
            total += import_project(project_dir)

    if total == 0:
        print("No new notes to import.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
