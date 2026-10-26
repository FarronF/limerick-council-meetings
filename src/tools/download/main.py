from datetime import datetime
from typing import List

from tools.download.get_meetings_from_website import get_public_meetings_for_year_month
from tools.download.meeting_files_downloader import MeetingFilesDownloader


def download_meeting_files(
    start_year: int,
    start_month: int,
    end_year: int,
    end_month: int,
    meeting_filter: List[str] = None,
    file_filter: List[str] = None,
    download_location: str = "./data/downloaded",
    redownload_existing: bool = False,
):
    print(f"Fetching meeting minutes from {start_year}-{start_month} to {end_year}-{end_month}...")
    if meeting_filter:
        print(f"Filtering meetings by name containing: '{meeting_filter}' (case insensitive)")
    if file_filter:
        print(f"Filtering files by name containing: '{file_filter}' (case insensitive)")

    current_date = datetime(start_year, start_month, 1)
    end_date = datetime(end_year, end_month, 1)
    downloader = MeetingFilesDownloader(destination_folder=download_location)

    while current_date <= end_date:
        meetings = get_public_meetings_for_year_month(
            current_date.year, current_date.month, meeting_filter
        )
        downloader.download_meeting_files_from_website(
            meetings,
            file_filter,
            redownload_existing=redownload_existing,
        )
        current_date = _add_month(current_date)


def _add_month(date: datetime) -> datetime:
    """Add one month to the given date."""
    if date.month == 12:
        return date.replace(year=date.year + 1, month=1)
    return date.replace(month=date.month + 1)
