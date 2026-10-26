"""Generate Pagefind metadata for published meeting documents."""
import argparse
import os
import re
import datetime

# Helper function to bypass Windows MAX_PATH limit
def get_win_safe_path(filepath):
    abs_path = os.path.abspath(filepath)
    if os.name == 'nt' and not abs_path.startswith('\\\\?\\'):
        return '\\\\?\\' + abs_path
    return abs_path

MEETINGS_DIR = "docs/meetings" if os.path.exists("docs/meetings") else "meetings"

MEETING_BODIES = [
    # --- Municipal Districts ---
    {
        "name": "Adare-Rathkeale",
        "category": "Municipal District",
        "synonyms": ["adare-rathkeale", "adare rathkeale", "adare - rathkeale", "adare_rathkeale"]
    },
    {
        "name": "Newcastle West",
        "category": "Municipal District",
        "synonyms": ["newcastle west", "newcastlewest", "newcastle-west", "newcastle_west"]
    },
    {
        "name": "Cappamore-Kilmallock",
        "category": "Municipal District",
        "synonyms": ["cappamore-kilmallock", "cappamore kilmallock", "cappamore - kilmallock", "cappamore_kilmallock"]
    },
    {
        "name": "Metropolitan District",
        "category": "Municipal District",
        "synonyms": ["metropolitan district", "metropolitan"]
    },

    # --- Full Council ---
    {
        "name": "Limerick City and County Council",
        "category": "Full Council",
        "synonyms": ["limerick city and county council", "full meeting", "plenary", "presidential election"]
    },

    # --- Committees ---
    {
        "name": "Community, Leisure & Emergency Services SPC",
        "category": "Committee",
        "synonyms": ["community leisure", "community, leisure"]
    },
    {
        "name": "Environment SPC",
        "category": "Committee",
        "synonyms": ["environment strategic policy", "environment spc", "spc for environment", "environment committee", "committee for environment"]
    },
    {
        "name": "Home & Social Development SPC",
        "category": "Committee",
        "synonyms": ["home & social", "home and social", "social development spc"]
    },
    {
        "name": "Travel & Transportation SPC",
        "category": "Committee",
        "synonyms": ["travel and transportation", "travel & transportation", "transportation spc"]
    },
    {
        "name": "Economic Development & Planning SPC",
        "category": "Committee",
        "synonyms": ["economic development", "enterprise and planning", "economic development, enterprise"]
    },
    {
        "name": "Cultural SPC",
        "category": "Committee",
        "synonyms": ["cultural spc", "cultural committee", "cultural strategic policy"]
    },
    {
        "name": "Joint Policing Committee",
        "category": "Committee",
        "synonyms": ["joint policing", "jpc"]
    }
]

# Tracking logs
unmatched_meetings = []
fallback_days = []
invalid_paths = []
io_errors = []
ignored_nav_readmes_count = 0

for root, dirs, files in os.walk(MEETINGS_DIR):
    for file in files:
        if not file.endswith(".md"):
            continue

        filepath = os.path.join(root, file)
        safe_filepath = get_win_safe_path(filepath)
        parts = os.path.relpath(filepath, MEETINGS_DIR).split(os.sep)

        # --- 1. HANDLE SHALLOW NAVIGATION/OVERVIEW PAGES ONLY ---
        is_shallow = len(parts) < 4
        is_nav_file = file.lower() in ["index.md", "search.md", "404.md"] or (file.lower() == "readme.md" and is_shallow)

        if is_nav_file:
            try:
                with open(safe_filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                clean_content = re.sub(r"^---\n.*?\n---\n+", "", content, flags=re.DOTALL)
                clean_content = re.sub(
                    r'<span data-pagefind-(filter|meta)="[^"]*" style="display:none;">.*?</span>\n?',
                    "",
                    clean_content,
                ).lstrip()

                ignore_header = "---\ndata-pagefind-ignore: true\n---\n\n"
                
                with open(safe_filepath, "w", encoding="utf-8") as f:
                    f.write(ignore_header + clean_content)
                
                ignored_nav_readmes_count += 1
                continue
            except Exception as e:
                io_errors.append((filepath, f"Failed adding ignore header: {str(e)}"))
                continue

        # --- 2. PROCESS DEEP MEETING FILES ---
        try:
            if is_shallow:
                invalid_paths.append((filepath, f"Path too shallow ({len(parts)} segments)"))
                continue

            year = parts[-4]
            month = parts[-3]
            day_folder = parts[-2]

            if not (re.match(r"^\d{4}$", year) and re.match(r"^\d{2}$", month)):
                invalid_paths.append((filepath, f"Folder structure not YYYY/MM: '{year}/{month}'"))
                continue

            # Extract day (first 2 digits)
            day_match = re.match(r"^(\d{2})", day_folder)
            if day_match:
                day = day_match.group(1)
            else:
                day = "01"
                fallback_days.append((filepath, day_folder))

            formatted_date = f"{year}-{month}-{day}"

            try:
                dt = datetime.datetime.strptime(formatted_date, "%Y-%m-%d")
                date_filter_val = dt.strftime("%Y-%m")
            except ValueError:
                date_filter_val = formatted_date

            folder_clean = re.sub(r"[\u200b\u2013\u2014]", "-", day_folder.lower())

            # --- DETERMINE MEETING TYPE ---
            if "annual" in folder_clean:
                meeting_type = "Annual"
            elif any(kw in folder_clean for kw in ["special", "extraordinary", "presentation", "presidential"]):
                meeting_type = "Special"
            else:
                meeting_type = "Regular"

            # --- DETERMINE BODY & CATEGORY ---
            matched_entity = None
            for body in MEETING_BODIES:
                if any(synonym in folder_clean for synonym in body["synonyms"]):
                    matched_entity = body
                    break

            if matched_entity:
                council_body = matched_entity["name"]
                category = matched_entity["category"]
            else:
                unmatched_meetings.append((filepath, day_folder))
                category = "Other"
                council_body = "Other"

            # Read content first to support Title extraction
            with open(safe_filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # Clean existing frontmatter and Pagefind HTML tags
            clean_content = re.sub(r"^---\n.*?\n---\n+", "", content, flags=re.DOTALL)
            clean_content = re.sub(
                r'<span data-pagefind-(filter|meta)="[^"]*" style="display:none;">.*?</span>\n?',
                "",
                clean_content,
            ).lstrip()

            # --- DETERMINE FILE TYPE & DYNAMIC TITLE ---
            file_lower = file.lower()
            if "agenda" in file_lower:
                file_type = "Agenda"
            elif "minute" in file_lower:
                file_type = "Minutes"
            elif file_lower == "readme.md":
                file_type = "Meeting Overview"
            else:
                file_type = "Document"

            # Extract title: If README, check for `# Title` heading, else use folder name. Otherwise use filename.
            if file_lower == "readme.md":
                h1_match = re.search(r"^#\s+(.+)$", clean_content, re.MULTILINE)
                if h1_match:
                    doc_title = h1_match.group(1).strip()
                else:
                    # Clean up folder name as title fallback
                    folder_title = re.sub(
                        r"^\d{2}\s+@\s+\d{2}-\d{2}\s+-\s*", "", day_folder
                    )
                    folder_title = re.sub(r"^\d{2}\s*[-_]?\s*", "", folder_title)
                    folder_title = re.sub(r"\s+@\s+\d{2}-\d{2}$", "", folder_title)
                    doc_title = folder_title.strip().title()
            else:
                doc_title = os.path.splitext(file)[0]

            safe_title = doc_title.replace('"', '\\"')

            # --- CONSTRUCT METADATA HEADER ---
            file_header = f"""---
title: "{safe_title}"
date: {formatted_date}
council_body: "{council_body}"
category: "{category}"
meeting_type: "{meeting_type}"
file_type: "{file_type}"
---

<span data-pagefind-meta="title" style="display:none;">{doc_title}</span>
<span data-pagefind-meta="date" style="display:none;">{formatted_date}</span>
<span data-pagefind-filter="Category" style="display:none;">{category}</span>
<span data-pagefind-filter="Council Body" style="display:none;">{council_body}</span>
<span data-pagefind-filter="Meeting Type" style="display:none;">{meeting_type}</span>
<span data-pagefind-filter="File Type" style="display:none;">{file_type}</span>
<span data-pagefind-filter="Year" style="display:none;">{year}</span>
<span data-pagefind-filter="Year-Month" style="display:none;">{date_filter_val}</span>

"""
            with open(safe_filepath, "w", encoding="utf-8") as f:
                f.write(file_header + clean_content)
            print(f"Updated: {filepath}")

        except IndexError:
            invalid_paths.append((filepath, "IndexError: Folder depth mismatch"))
        except Exception as e:
            io_errors.append((filepath, str(e)))

# --- CONSOLE SUMMARY & LOG WRITER ---
print("\n" + "="*60)
print("TAGGING PROCESS COMPLETE")
print("="*60)
print(f"⚠️ Shallow Navigation READMEs Ignored: {ignored_nav_readmes_count}")
print(f"⚠️ Unmatched names (Clean Fallback Applied): {len(unmatched_meetings)}")
print(f"⚠️ Missing day digits (Defaulted to 01): {len(fallback_days)}")
print(f"❌ Invalid paths: {len(invalid_paths)}")
print(f"❌ IO Errors: {len(io_errors)}")

parser = argparse.ArgumentParser()
parser.add_argument("--logs-location", default="./.logs")
args = parser.parse_args()
os.makedirs(args.logs_location, exist_ok=True)
log_path = os.path.join(args.logs_location, "tagging_errors.log")

with open(log_path, "w", encoding="utf-8") as log_file:
    log_file.write(f"=== UNMATCHED MEETINGS ({len(unmatched_meetings)}) ===\n")
    for path, folder in unmatched_meetings:
        log_file.write(f"Folder: '{folder}' -> File: {path}\n")

    log_file.write(f"\n=== FALLBACK DAYS ({len(fallback_days)}) ===\n")
    for path, folder in fallback_days:
        log_file.write(f"Folder: '{folder}' -> File: {path}\n")

    log_file.write(f"\n=== INVALID PATHS ({len(invalid_paths)}) ===\n")
    for path, reason in invalid_paths:
        log_file.write(f"Reason: {reason} -> File: {path}\n")

print(f"\nDetailed log saved to '{log_path}'.")