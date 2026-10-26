from pathlib import Path
import calendar

# Resolve paths relative to repo root
ROOT_DIR = Path(__file__).resolve().parents[3]
MEETINGS_DIR = ROOT_DIR / "docs" / "meetings"
PAGEFIND_IGNORE_HEADER = "---\ndata-pagefind-ignore: true\n---\n\n"

def generate_archive_readmes():
    if not MEETINGS_DIR.exists():
        print(f"❌ Meetings directory not found at {MEETINGS_DIR}")
        return

    print("🔄 Generating README.md files for archive hierarchy...")

    root_links = []

    # 1. Find all Year folders (e.g., 2024, 2025, 2026)
    years = sorted([p for p in MEETINGS_DIR.iterdir() if p.is_dir() and p.name.isdigit() and len(p.name) == 4], reverse=True)

    for year_dir in years:
        year_name = year_dir.name
        root_links.append(f"**[{year_name} Archive]({year_name}/README.md)**")

        month_links = []
        # 2. Find months inside the year folder
        months = sorted([p for p in year_dir.iterdir() if p.is_dir()])

        for month_dir in months:
            month_name = month_dir.name
            display_name = month_name.replace("-", " ").title()
            
            # Format month nicely if it starts with digits (e.g. "01" -> "01 - January")
            if month_name[:2].isdigit():
                try:
                    m_num = int(month_name[:2])
                    if 1 <= m_num <= 12:
                        display_name = f"{month_name[:2]} - {calendar.month_name[m_num]}"
                except ValueError:
                    pass

            month_links.append(f"**[{display_name}]({month_name}/README.md)**")

            # 3. Find individual meetings/files inside the month folder
            meeting_links = []
            for item in sorted(month_dir.iterdir()):
                if item.name.lower() == "readme.md":
                    continue
                
                clean_title = item.stem.replace("-", " ").title()
                if item.is_file() and item.suffix == ".md":
                    meeting_links.append(f"* [{clean_title}]({item.name})")
                elif item.is_dir():
                    meeting_links.append(f"* [{clean_title}]({item.name}/README.md)")

            # Write Month README
            month_readme = month_dir / "README.md"
            month_content = PAGEFIND_IGNORE_HEADER + f"# {year_name} — {display_name}\n\n" + (
                "\n\n".join(meeting_links) if meeting_links else "*No individual meetings recorded for this month.*"
            )
            month_readme.write_text(month_content, encoding="utf-8")

        # Write Year README
        year_readme = year_dir / "README.md"
        year_content = PAGEFIND_IGNORE_HEADER + f"# {year_name} Council Meetings\n\nSelect a month to view records:\n\n" + (
            "\n\n".join(month_links) if month_links else "*No months recorded for this year.*"
        )
        year_readme.write_text(year_content, encoding="utf-8")

    # 4. Write Root Meetings README
    root_readme = MEETINGS_DIR / "README.md"
    root_content = PAGEFIND_IGNORE_HEADER + f"# Council Meetings Archive\n\nSelect a year to browse records:\n\n" + (
        "\n\n".join(root_links) if root_links else "*No year archives available.*"
    )
    root_readme.write_text(root_content, encoding="utf-8")

    print("✅ Successfully generated all archive READMEs!")

if __name__ == "__main__":
    generate_archive_readmes()