import requests


def content_in_html(url, content):
    response = requests.get(url)
    if content in response.text:
        return True
    else:
        return True
