import json
import os
import re
from pathlib import Path
from typing import List

from bs4 import BeautifulSoup

from tools.download.fetch_web_content import fetch_web_content
from tools.download.pdf_downloader import download_pdf_to_folder
from tools.shared.file_logger import FileLoggerSingleton
from tools.shared.types.meeting_details import MeetingDetails


MAX_FILE_NAME_LENGTH = 255
FILE_NAME_TRUNCATION_SUFFIX = " [truncated]"


class MeetingFilesDownloader:
    def __init__(self, destination_folder: str = None):
        self.destination_folder = (
            Path(destination_folder) if destination_folder else Path.cwd() / "data/meetings"
        )

    def download_meeting_files_from_website(
        self,
        meetings: List[MeetingDetails],
        file_filters: List[str] = None,
        redownload_existing: bool = False,
    ):
        if meetings is None or len(meetings) == 0:
            return

        for meeting in meetings:
            meeting_datetime = meeting["datetime"]
            folder_name = re.sub(r'[\\/*?:"<>|]', "_", meeting["meeting_name"])
            destination_path = (
                self.destination_folder
                / f"{meeting_datetime.year}"
                / f"{meeting_datetime.month:02d}"
                / (
                    f"{meeting_datetime.day:02d} @ {meeting_datetime:%H-%M} "
                    f"- {folder_name}"
                )
            )
            os.makedirs(destination_path, exist_ok=True)

            meeting_page_html = fetch_web_content(meeting["href"])
            if meeting_page_html is None:
                continue

            soup = BeautifulSoup(meeting_page_html, "html.parser")
            links = soup.find_all(
                "a",
                href=lambda href: href and href.endswith(".pdf"),
            )

            files = []
            for link in links:
                display_text = link.string.strip() if link.string else "document"
                safe_file_stem = re.sub(r'[\\/*?:"<>|]', "_", display_text) or "document"
                file_name = f"{safe_file_stem}.pdf"
                max_file_stem_length = (
                    MAX_FILE_NAME_LENGTH
                    - len(FILE_NAME_TRUNCATION_SUFFIX)
                    - len(".pdf")
                )
                if len(file_name) > MAX_FILE_NAME_LENGTH:
                    file_name = (
                        safe_file_stem[:max_file_stem_length]
                        + FILE_NAME_TRUNCATION_SUFFIX
                        + ".pdf"
                    )
                    FileLoggerSingleton._instance.log(
                        "file_name_truncated",
                        f"Original: {safe_file_stem}.pdf\nShortened: {file_name}",
                    )

                file = {
                    "display_text": display_text,
                    "file_name": file_name,
                    "url": link.get("href"),
                    "downloaded": False,
                }

                if not file_filters or any(
                    filter_word.lower() in display_text.lower() for filter_word in file_filters
                ):
                    pdf_path = destination_path / file_name
                    if not redownload_existing and pdf_path.exists():
                        print(f"Already downloaded, skipping: {pdf_path}")
                        download_success = True
                    else:
                        download_success = download_pdf_to_folder(
                            link, destination_path, file_name
                        )
                    file["downloaded"] = download_success
                    if not download_success:
                        self._log_failed_download(destination_path, file["url"])

                files.append(file)

            meeting["files"] = files
            json_file_path = os.path.join(destination_path, "meeting_details.json")
            with open(json_file_path, "w", encoding="utf-8") as json_file:
                json.dump(meeting, json_file, indent=4, default=str)

    def _log_failed_download(self, folder_path, failed_download):
        FileLoggerSingleton._instance.log(
            "failed_download", f"{folder_path}, {failed_download}"
        )
