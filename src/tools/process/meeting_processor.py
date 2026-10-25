import json
import os
from typing import List
from urllib.parse import quote

from tools.process.pdf_processors.fitz_processor import FitzProcessor


MEETING_README_TEMPLATE = """# Meeting Details

**Meeting Name:** {meeting_name}

**Date and Time:** {datetime}

**[Link to Meeting]({href})**

Files:

"""


class MeetingProcessor:
    def process_meeting(
        self, meeting_folder: str, output_meeting_folder: str, file_filter: List[str] = None
    ):
        """Process a meeting folder and generate Markdown files."""
        print(f"Processing meeting: {meeting_folder}")
        meeting_details_path = os.path.join(meeting_folder, "meeting_details.json")
        if not os.path.exists(meeting_details_path):
            return

        with open(meeting_details_path, "r", encoding="utf-8") as details_file:
            meeting_details = json.load(details_file)

        os.makedirs(output_meeting_folder, exist_ok=True)
        readme_content = MEETING_README_TEMPLATE.format(
            meeting_name=meeting_details["meeting_name"],
            datetime=meeting_details["datetime"],
            href=meeting_details["href"],
        )

        files_info = meeting_details.get("files", [])
        if not files_info:
            readme_content += "No files available for this meeting."

        for file_info in files_info:
            file_name = file_info.get("file_name")
            file_url = file_info.get("url", "#")
            downloaded = file_info.get("downloaded")
            processed = False
            md_file_name = None

            if (
                downloaded
                and file_name
                and file_name.endswith(".pdf")
                and (
                    file_filter is None
                    or any(filter_word.lower() in file_name.lower() for filter_word in file_filter)
                )
            ):
                pdf_file_path = os.path.join(meeting_folder, file_name)
                if os.path.exists(pdf_file_path):
                    processed = self._process_pdf(
                        pdf_file_path, output_meeting_folder, file_url
                    )
                    md_file_name = f"{os.path.splitext(os.path.basename(pdf_file_path))[0]}.md"
                else:
                    print(f"File {pdf_file_path} not found, skipping PDF processing.")

            readme_content += f"{file_name} - [Original file]({file_url})"
            if processed and md_file_name:
                readme_content += f" - [Extracted text](./{quote(md_file_name)})"
            else:
                readme_content += " - Text not extracted"
            readme_content += "\n\n"

        readme_path = os.path.join(output_meeting_folder, "README.md")
        with open(readme_path, "w", encoding="utf-8") as readme_file:
            readme_file.write(readme_content)

    def _process_pdf(self, pdf_path, output_folder, original_url):
        print(f"Processing PDF: {os.path.basename(pdf_path)}")
        try:
            markdown_output = FitzProcessor().process(pdf_path)
            if markdown_output:
                markdown_output = f"[Original file]({original_url})\n\n---\n" + markdown_output
                self._save_markdown(markdown_output, pdf_path, output_folder)
            else:
                print(f"No content extracted from {pdf_path}.")
                return False
        except Exception as error:
            print(f"Error processing {pdf_path}: {error}")
            return False
        return True

    def _save_markdown(self, markdown_content, pdf_path, output_folder):
        """Save extracted Markdown next to the meeting summary."""
        output_md_path = os.path.join(
            output_folder, f"{os.path.splitext(os.path.basename(pdf_path))[0]}.md"
        )
        with open(output_md_path, "w", encoding="utf-8") as md_file:
            md_file.write(markdown_content)
