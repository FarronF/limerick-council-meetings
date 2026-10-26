import os
from typing import List

from tools.process.meeting_processor import MeetingProcessor


def process_meetings(
    start_year: int,
    start_month: int,
    end_year: int,
    end_month: int,
    meeting_filter: List[str] = None,
    file_filter: List[str] = None,
    download_location: str = "./data/downloaded",
    output_location: str = "./data/processed",
    reprocess_existing: bool = False,
):
    """Process downloaded PDFs and return meeting folders written this run."""
    input_folder = os.path.abspath(download_location)
    output_folder = os.path.abspath(output_location)
    meeting_processor = MeetingProcessor()
    os.makedirs(output_folder, exist_ok=True)
    processed_meetings = []

    for year in range(start_year, end_year + 1):
        year_path = os.path.join(input_folder, str(year))
        if not os.path.exists(year_path):
            print(f"Year folder {year_path} does not exist, skipping year {year}.")
            continue

        start_month_range = start_month if year == start_year else 1
        end_month_range = end_month if year == end_year else 12

        for month in range(start_month_range, end_month_range + 1):
            month_folder = f"{month:02d}"
            month_path = os.path.join(year_path, month_folder)
            if not os.path.exists(month_path):
                print(f"Month folder {month_path} does not exist, skipping month {month}.")
                continue

            for meeting_folder in sorted(os.listdir(month_path)):
                meeting_folder_path = os.path.join(month_path, meeting_folder)
                output_meeting_folder = os.path.join(
                    output_folder, str(year), month_folder, meeting_folder
                )
                if os.path.isdir(meeting_folder_path) and (
                    meeting_filter is None
                    or any(
                        filter_word.lower() in meeting_folder.lower()
                        for filter_word in meeting_filter
                    )
                ):
                    if meeting_processor.process_meeting(
                        meeting_folder_path,
                        output_meeting_folder,
                        file_filter,
                        reprocess_existing=reprocess_existing,
                    ):
                        processed_meetings.append(output_meeting_folder)

    return processed_meetings
