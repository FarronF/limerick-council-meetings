from pathlib import Path
import shutil
import subprocess
import sys
from typing import Iterable


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
POSTPROCESSING_SCRIPTS = (
    "rename_readmes.py",
    "generate_readme.py",
    "clean_page_markers.py",
    "tag.py",
)


def find_processed_meetings(
    processed_root: str | Path,
    start_year: int,
    start_month: int,
    end_year: int,
    end_month: int,
    meeting_filter: list[str] | None = None,
) -> list[Path]:
    """Find existing processed meeting folders within the requested range."""
    processed_root = Path(processed_root).resolve()
    meetings = []

    for year in range(start_year, end_year + 1):
        first_month = start_month if year == start_year else 1
        last_month = end_month if year == end_year else 12
        for month in range(first_month, last_month + 1):
            month_path = processed_root / str(year) / f"{month:02d}"
            if not month_path.is_dir():
                continue

            for meeting_path in sorted(month_path.iterdir()):
                if not meeting_path.is_dir() or not (meeting_path / "README.md").is_file():
                    continue
                if meeting_filter and not any(
                    keyword.lower() in meeting_path.name.lower()
                    for keyword in meeting_filter
                ):
                    continue
                meetings.append(meeting_path)

    return meetings


def publish_processed_meetings(
    processed_meetings: Iterable[str | Path],
    processed_root: str | Path = "./data/processed",
    meetings_root: str | Path = "./docs/meetings",
    logs_location: str | Path = "./.logs",
    republish_existing: bool = False,
) -> tuple[int, int]:
    """Copy meetings processed during this run, then prepare the published archive."""
    processed_root = Path(processed_root).resolve()
    meetings_root = Path(meetings_root).resolve()
    logs_location = Path(logs_location).resolve()
    meeting_paths = sorted({Path(path).resolve() for path in processed_meetings})
    if not meeting_paths:
        return 0, 0

    copied = 0
    unchanged = 0
    for source_meeting in meeting_paths:
        try:
            relative_meeting = source_meeting.relative_to(processed_root)
        except ValueError as error:
            raise ValueError(
                f"Processed meeting is outside the processed root: {source_meeting}"
            ) from error

        if len(relative_meeting.parts) != 3:
            raise ValueError(
                "Processed meetings must be under YEAR/MONTH/MEETING: "
                f"{source_meeting}"
            )
        if not source_meeting.is_dir():
            raise FileNotFoundError(f"Processed meeting folder not found: {source_meeting}")

        destination_meeting = meetings_root / relative_meeting
        for source_file in sorted(path for path in source_meeting.rglob("*") if path.is_file()):
            relative_file = source_file.relative_to(source_meeting)
            destination_file = destination_meeting / relative_file
            if destination_file.is_file() and not republish_existing:
                unchanged += 1
                continue

            destination_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_file, destination_file)
            copied += 1

    print(f"Published {copied} file(s); left {unchanged} unchanged.")
    if copied:
        run_postprocessing(logs_location)
    return copied, unchanged


def run_postprocessing(logs_location: Path = Path("./.logs")):
    script_directory = Path(__file__).resolve().parent
    for script_name in POSTPROCESSING_SCRIPTS:
        script_path = script_directory / script_name
        if not script_path.is_file():
            raise FileNotFoundError(f"Post-processing script not found: {script_path}")
        print(f"Running {script_name}...")
        command = [sys.executable, str(script_path)]
        if script_name == "tag.py":
            command.extend(["--logs-location", str(logs_location)])
        subprocess.run(
            command,
            cwd=REPOSITORY_ROOT,
            check=True,
        )
