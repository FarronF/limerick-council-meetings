import os
from pathlib import Path
import re

import requests


def download_pdf_to_folder(link, folder_path: Path, file_name: str = None):
    os.makedirs(folder_path, exist_ok=True)
    url = link.get("href")
    link_text = str(link.string).strip() if link.string else "document"
    safe_filename = file_name or (re.sub(r'[\\/*?:"<>|]', "_", link_text) + ".pdf")
    file_path = os.path.join(folder_path, safe_filename)

    try:
        print(f"Downloading: {url} to {file_path}")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)

        print(f"Downloaded: {file_path}")
    except requests.exceptions.RequestException as error:
        print(f"Failed to download {url}: {error}")
        return False
    return True
