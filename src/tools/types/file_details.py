from typing import TypedDict


class FileDetails(TypedDict):
    display_text: str
    file_name: str
    url: str
    downloaded: bool
