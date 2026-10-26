"""Legacy date metadata helper; tag.py already writes Pagefind dates."""
import os
import re
import yaml
from pathlib import Path

# Resolve directory path relative to the script's actual location
ROOT_DIR = Path(__file__).resolve().parents[3]
MEETINGS_DIR = ROOT_DIR / "docs" / "meetings"

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Match YAML frontmatter between top --- markers
    yaml_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not yaml_match:
        return

    yaml_text = yaml_match.group(1)
    try:
        data = yaml.safe_load(yaml_text)
    except Exception as e:
        print(f"Error parsing YAML in {file_path}: {e}")
        return

    # Extract date from frontmatter
    date_val = data.get("date")
    if not date_val:
        return

    # Format date string consistently (YYYY-MM-DD)
    date_str = str(date_val).strip()

    # Check if data-pagefind-meta="date" already exists
    if 'data-pagefind-meta="date"' in content:
        # Update existing meta tag if date changed
        updated_content = re.sub(
            r'<span data-pagefind-meta="date"[^>]*>.*?</span>',
            f'<span data-pagefind-meta="date" style="display:none;">{date_str}</span>',
            content
        )
    else:
        # Insert meta tag after the last data-pagefind-filter span
        target_pattern = r'(<span data-pagefind-filter="Year-Month"[^>]*>.*?</span>)'
        new_tag = f'\n<span data-pagefind-meta="date" style="display:none;">{date_str}</span>'

        if re.search(target_pattern, content):
            updated_content = re.sub(target_pattern, rf'\1{new_tag}', content, count=1)
        else:
            # Fallback: attach to end of YAML block if no Year-Month tag exists
            yaml_block_end = yaml_match.end()
            updated_content = content[:yaml_block_end] + f'{new_tag}\n' + content[yaml_block_end:]

    if updated_content != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"Updated date meta for: {file_path}")

def main():
    print(f"Target directory resolved to: {MEETINGS_DIR}")
    
    if not os.path.exists(MEETINGS_DIR):
        print(f"ERROR: Directory does not exist: {MEETINGS_DIR}")
        return

    file_count = 0
    for root, _, files in os.walk(MEETINGS_DIR):
        for file in files:
            if file.endswith((".md", ".html")):
                file_count += 1
                process_file(os.path.join(root, file))
                
    print(f"Finished processing. Scanned {file_count} files.")

if __name__ == "__main__":
    main()