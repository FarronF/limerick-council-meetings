import requests


def fetch_web_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as error:
        print(f"An error occurred: {error}")
        return None
