"""Legacy cleanup helper; the publish pipeline performs its own normalization."""
import os
import re

MEETINGS_DIR = "docs/meetings" if os.path.exists("docs/meetings") else "meetings"

cleaned_count = 0

for root, dirs, files in os.walk(MEETINGS_DIR):
    for file in files:
        if file.lower() == "readme.md":
            filepath = os.path.join(root, file)
            
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # 1. Strip YAML frontmatter if present
            clean_content = re.sub(r"^---\n.*?\n---\n+", "", content, flags=re.DOTALL)

            # 2. Strip Pagefind HTML filter spans if present
            clean_content = re.sub(
                r'<span data-pagefind-filter="[^"]*" style="display:none;">.*?</span>\n?',
                "",
                clean_content,
                flags=re.DOTALL,
            )

            clean_content = clean_content.lstrip()

            # Only write back if changes were actually made
            if clean_content != content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(clean_content)
                print(f"Stripped tags from: {filepath}")
                cleaned_count += 1

print(f"\nCleanup complete. Successfully cleaned {cleaned_count} README.md file(s).")