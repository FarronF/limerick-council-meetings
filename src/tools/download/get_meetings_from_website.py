from datetime import datetime
import json
from typing import List

from bs4 import BeautifulSoup

from tools.download.fetch_web_content import fetch_web_content
from tools.types.meeting_details import MeetingDetails


def get_public_meetings_for_year_month(
    year: int, month: int, meeting_filter_keywords: List[str] = None
) -> List[MeetingDetails]:
    calendar_ajax_url = (
        "https://www.limerick.ie/views/ajax?view_name=council_meetings_calendar"
        f"&view_display_id=page_month&view_args={year}{month:02d}"
    )
    print(f"Fetching data for {year}-{month:02d}...")
    content = fetch_web_content(calendar_ajax_url)

    if not content:
        return None

    html = _get_calendar_html(content)
    meetings = _get_public_meetings_from_html(html, meeting_filter_keywords)
    print(f"Found {len(meetings)} meetings for {year}-{month:02d}.")
    return meetings


def _get_public_meetings_from_html(
    html: str, filter_keywords: List[str] = None
) -> List[MeetingDetails]:
    soup = BeautifulSoup(html, "html.parser")
    meeting_details: List[MeetingDetails] = []

    for item in soup.find_all("div", class_="view-item"):
        link_tag = item.find(
            "a",
            string=lambda text: text and not text.strip().startswith("PRIVATE"),
            href=lambda href: href and href.startswith("/council/whats-on"),
        )
        time_tag = item.find("time", class_="datetime")

        if link_tag and time_tag:
            meeting_name = link_tag.contents[0].strip()
            if not filter_keywords or any(
                keyword.lower() in meeting_name.lower() for keyword in filter_keywords
            ):
                meeting_details.append(
                    {
                        "meeting_name": meeting_name,
                        "href": f"https://www.limerick.ie{link_tag['href']}",
                        "datetime": datetime.strptime(
                            time_tag["datetime"], "%Y-%m-%dT%H:%M:%SZ"
                        ),
                    }
                )
                print(meeting_name, link_tag["href"], time_tag["datetime"])

    return meeting_details


def _get_calendar_html(response: str) -> str:
    parsed_response = json.loads(response)
    return parsed_response[3]["data"]
