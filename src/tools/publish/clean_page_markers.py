import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
MEETINGS_DIR = ROOT_DIR / "docs" / "meetings"
MARKER_PATTERN = re.compile(r"(?m)^[ \t]*(\[\[(?:FILE_START|PAGE_END:\d+)\]\])[ \t]*\r?$")


def main():
    if not MEETINGS_DIR.exists():
        print(f"Meetings directory not found: {MEETINGS_DIR}")
        return

    files_updated = 0
    markers_wrapped = 0

    for file_path in MEETINGS_DIR.rglob("*.md"):
        with file_path.open("r", encoding="utf-8", newline="") as file:
            content = file.read()

        updated_content, wrapped_count = MARKER_PATTERN.subn(
            r'<span data-pagefind-ignore>\1</span>', content
        )
        if wrapped_count:
            with file_path.open("w", encoding="utf-8", newline="") as file:
                file.write(updated_content)
            files_updated += 1
            markers_wrapped += wrapped_count
            print(f"Wrapped {wrapped_count} marker(s) for Pagefind: {file_path}")

    print(f"\nCleanup complete. Updated {files_updated} file(s); wrapped {markers_wrapped} marker(s).")


if __name__ == "__main__":
    main()