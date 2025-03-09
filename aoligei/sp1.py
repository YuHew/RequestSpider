import asyncio

import requests

from base.config import config

BASE_URL_AJX = 'https://spa2.scrape.center/api/movie/?limit=10&offset='
BASE_URL_DETAIL_AJX = 'https://spa2.scrape.center/api/movie/'
headers = {'User-Agent': config.user_agent}


def process_page():
    urls = []
    for i in range(0, 11):
        urls.append(BASE_URL_AJX + str(i * 10))
    return urls


def main():
    pages_url = process_page()

    for page in pages_url:
        page_data = requests.get(page, headers=headers)
        json_data = page_data.json()
        print(json_data)

        for item in json_data.get('results'):
                id = item.get('id')
                response = requests.get(BASE_URL_DETAIL_AJX + str(id), headers=headers)
                detail_data = response.json()
                print(detail_data)

if __name__ == '__main__':
    main()



