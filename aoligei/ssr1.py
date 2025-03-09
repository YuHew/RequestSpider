# https://ssr1.scrape.center/

import requests
from lxml import etree
from base.config import config


class Film:

    def __init__(self, title, typeof, where, duration, time, pic, score, star, instruction):
        self.title = title
        self.typeof = typeof
        self.where = where
        self.duration = duration
        self.time = time
        self.pic = pic
        self.score = score
        self.star = star
        self.instruction = instruction

    def __str__(self):
        return f'title: {self.title}, typeof: {self.typeof}, where: {self.where}, duration: {self.duration}, time: {self.time}, pic: {self.pic}, score: {self.score}, star: {self.star}, instruction: {self.instruction}\n'

    def __repr__(self):
        return f'title: {self.title}, typeof: {self.typeof}, where: {self.where}, duration: {self.duration}, time: {self.time}, pic: {self.pic}, score: {self.score}, star: {self.star}, instruction: {self.instruction}\n'


BASE_URL = 'https://ssr4.scrape.center'
next_url = BASE_URL
headers = {'User-Agent': config.user_agent}


def get_data(url):
    return requests.get(url, headers=headers, auth=('admin', 'admin'), timeout=10)


def parse_page_data(response_text):
    html = etree.HTML(response_text)
    get_next_url(html)

    if len(html.xpath('//*[@id="index"]/div[1]/div[1]')) == 0:
        return None

    div_list = html.xpath('//*[@id="index"]/div[1]/div[1]')[0]
    child_div = div_list.xpath('./div')
    page_detail_urls = []
    for div in child_div:
        page_detail_urls.append(BASE_URL + div.xpath(f'./div/div/div[2]/a/@href')[0])

    return page_detail_urls


def parse_detail_data(response_text):
    html = etree.HTML(response_text)

    title_list = html.xpath("//*[@id='detail']/div[1]/div/div/div[1]/div/div[2]/a/h2/text()")
    title = title_list[0] if title_list else None

    typeof_list = html.xpath('//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/div[1]')[0]
    types = list(map(lambda signel_type: signel_type.xpath(f'./span/text()'), typeof_list))

    where_list = html.xpath("//*[@id='detail']/div[1]/div/div/div[1]/div/div[2]/div[2]/span[1]/text()")
    where = where_list[0] if where_list else None

    duration_list = html.xpath("//*[@id='detail']/div[1]/div/div/div[1]/div/div[2]/div[2]/span[3]/text()")
    duration = duration_list[0] if duration_list else None

    instruction_list = html.xpath("//*[@id='detail']/div[1]/div/div/div[1]/div/div[2]/div[4]/p/text()")
    instruction = instruction_list[0] if instruction_list else None

    time_list = html.xpath("//*[@id='detail']/div[1]/div/div/div[1]/div/div[2]/div[3]/span/text()")
    time = time_list[0] if time_list else None

    pic_list = html.xpath("//*[@id='detail']/div[1]/div/div/div[1]/div/div[1]/a/img/@src")
    pic = pic_list[0] if pic_list else None

    score_list = html.xpath("//*[@id='detail']/div[1]/div/div/div[1]/div/div[3]/p[1]/text()")
    score = score_list[0].replace('\n', '').strip() if score_list else None

    star_list = html.xpath("//*[@id='detail']/div[1]/div/div/div[1]/div/div[3]/div/@aria-valuenow")
    star = star_list[0] if star_list else None

    film = Film(title, types, where, duration, time, pic, score, star, instruction)
    return film


def get_next_url(html):
    global next_url
    try:
        next_a = html.xpath("//*[@id='index']/div[2]/div/div/div/a")
        if len(next_a) == 1:
            next_url = BASE_URL + next_a[0].get('href')
        else:
            next_url = BASE_URL + next_a[1].get('href')
        print(next_url)
    except Exception as e:
        next_url = None
        print(e)


def main():
    detail_url_list = []
    films = []

    while True:
        response = get_data(next_url)
        if response.status_code == 200:
            detail_urls = parse_page_data(response.text)
            detail_url_list.extend(detail_urls)
            print(detail_url_list)
        else:
            print(f'detail_urls请求异常，返回码：{response.status_code}')
            break


    for detail_url in detail_url_list:
        response = get_data(detail_url)
        if response.status_code == 200:
            films_detail = parse_detail_data(response.text)
            films.append(films_detail)
            print(films_detail)
        else:
            print(f'detail_url请求异常，返回码：{response.status_code}')
            break

    with open('detail_url.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(str(film) for film in films))


if __name__ == '__main__':
    main()

