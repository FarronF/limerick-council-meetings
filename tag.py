import os
import re

MEETINGS_DIR = "meetings"  # Change if your root directory differs

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
already_tagged = []
io_errors = []

for root, dirs, files in os.walk(MEETINGS_DIR):
    for file in files:
        if file.endswith(".md") and file != "index.md" and file != "search.md":
            filepath = os.path.join(root, file)
            parts = os.path.normpath(filepath).split(os.sep)

            try:
                if len(parts) < 4:
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

                # Sanitize folder name for hidden spaces/dashes
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
                    body_name = matched_entity["name"]
                    category = matched_entity["category"]
                else:
                    unmatched_meetings.append((filepath, day_folder))
                    
                    # Clean generic fallbacks instead of raw folder strings
                    if "district" in folder_clean:
                        category = "Municipal District"
                        body_name = "Municipal District"
                    elif any(kw in folder_clean for kw in ["spc", "committee", "jpc", "policing"]):
                        category = "Committee"
                        body_name = "Council Committee"
                    else:
                        category = "Full Council"
                        body_name = "Limerick City and County Council"

                # Read content
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                if content.startswith("---"):
                    already_tagged.append(filepath)
                    continue

                # Construct YAML frontmatter
                frontmatter = f"""---
date: {formatted_date}
body: "{body_name}"
category: "{category}"
meeting_type: "{meeting_type}"
tags:
  - "{body_name}"
  - "{category}"
  - "{meeting_type}"
---

"""
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(frontmatter + content)
                print(f"Updated: {filepath}")

            except IndexError:
                invalid_paths.append((filepath, "IndexError: Folder depth mismatch"))
            except Exception as e:
                io_errors.append((filepath, str(e)))

# --- CONSOLE SUMMARY & LOG WRITER ---
print("\n" + "="*60)
print("TAGGING PROCESS COMPLETE")
print("="*60)
print(f"✅ Already tagged (Skipped): {len(already_tagged)}")
print(f"⚠️  Unmatched names (Clean Fallback Applied): {len(unmatched_meetings)}")
print(f"⚠️  Missing day digits (Defaulted to 01): {len(fallback_days)}")
print(f"❌ Invalid paths: {len(invalid_paths)}")
print(f"❌ IO Errors: {len(io_errors)}")

with open("tagging_errors.log", "w", encoding="utf-8") as log_file:
    log_file.write(f"=== UNMATCHED MEETINGS ({len(unmatched_meetings)}) ===\n")
    for path, folder in unmatched_meetings:
        log_file.write(f"Folder: '{folder}' -> File: {path}\n")

    log_file.write(f"\n=== FALLBACK DAYS ({len(fallback_days)}) ===\n")
    for path, folder in fallback_days:
        log_file.write(f"Folder: '{folder}' -> File: {path}\n")

    log_file.write(f"\n=== INVALID PATHS ({len(invalid_paths)}) ===\n")
    for path, reason in invalid_paths:
        log_file.write(f"Reason: {reason} -> File: {path}\n")

print("\nDetailed log saved to 'tagging_errors.log'.")