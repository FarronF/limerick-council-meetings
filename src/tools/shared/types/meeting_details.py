from datetime import datetime
from typing import List, TypedDict

from tools.shared.types.file_details import FileDetails


class MeetingDetails(TypedDict):
    meeting_name: str
    href: str
    datetime: datetime
    files: List[FileDetails]
