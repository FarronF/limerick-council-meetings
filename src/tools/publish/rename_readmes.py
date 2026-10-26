"""Normalize meeting overview headings before Pagefind metadata is generated."""
import os
import re

# Update path to match your directory setup
MEETINGS_DIR = "docs/meetings" if os.path.exists("docs/meetings") else "meetings"

updated_count = 0

for root, dirs, files in os.walk(MEETINGS_DIR):
    for file in files:
        if not file.endswith(".md"):
            continue

        filepath = os.path.join(root, file)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # Captures Group 1: Meeting Name, Group 2: Date and Time
            pattern = (
                r"# Meeting Details\s*\n+"
                r"\*\*Meeting Name:\*\*\s*(.+)\s*\n+"
                r"\*\*Date and Time:\*\*\s*(.+)"
            )

            match = re.search(pattern, content)
            if match:
                meeting_name = match.group(1).strip()
                date_time = match.group(2).strip()

                # Title becomes the meeting name, keeping only the Date and Time below
                new_header = (
                    f"# {meeting_name}\n\n"
                    f"**Date and Time:** {date_time}"
                )

                # Replace the old section
                updated_content = re.sub(pattern, new_header, content)

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(updated_content)

                updated_count += 1
                print(f"Updated header in: {filepath}")

        except Exception as e:
            print(f"Error processing {filepath}: {e}")

print("\n" + "="*50)
print(f"Header update complete. Total files processed: {updated_count}")
print("="*50)