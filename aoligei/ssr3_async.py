# https://ssr1.scrape.center/
import json

from lxml import etree
import asyncio
from aiohttp import BasicAuth, ClientSession, ClientTimeout
from base.config import config

BASE_URL = 'https://ssr4.scrape.center'
next_url = BASE_URL
headers = {'User-Agent': config.user_agent}
CONCURRENCY = 10  # 并发数量控制


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


def parse_all_pages(response_text):
    html = etree.HTML(response_text)
    pages_list = html.xpath("//*[@id='index']/div[2]/div/div/div/ul/li")
    page_url_list = []
    for page in pages_list:
        page_urls = page.xpath("./a/@href")
        page_url = page_urls[0] if page_urls else None
        page_url_list.append(BASE_URL + page_url)
    return page_url_list


def parse_page_data(response_text):
    html = etree.HTML(response_text)

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


async def fetch(session, url):
    """通用异步请求函数"""
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.text()
    except Exception as e:
        print(f"请求失败 {url}: {e}")
        return None


async def get_all_page_urls(session):
    """异步获取所有分页URL"""
    text = await fetch(session, BASE_URL)
    if not text:
        return []
    return parse_all_pages(text)


async def process_page(session, page_url, detail_urls, sem):
    """处理单个分页，提取详情页URL"""
    async with sem:  # 控制并发量
        text = await fetch(session, page_url)
        if text:
            detail_urls.extend(parse_page_data(text))
        print(detail_urls)


async def process_detail(session, detail_url, films, sem):
    """处理单个详情页"""
    async with sem:
        text = await fetch(session, detail_url)
        if text:
            films.append(parse_detail_data(text))
        print(films)


async def main():
    # 使用一个全局session提升性能
    async with ClientSession(
        headers=headers,
        auth=BasicAuth('admin', 'admin'),
        timeout=ClientTimeout(10)
    ) as session:
        # 异步获取所有分页URL
        page_urls = await get_all_page_urls(session)
        print(f"共获取 {len(page_urls)} 个分页")
        # 并发处理所有分页
        detail_urls = []
        sem_page = asyncio.Semaphore(CONCURRENCY)
        tasks = [
            asyncio.create_task(process_page(session, url, detail_urls, sem_page))
            for url in page_urls
        ]
        await asyncio.gather(*tasks)
        # 并发处理所有详情页
        films = []
        sem_detail = asyncio.Semaphore(CONCURRENCY)
        tasks = [
            asyncio.create_task(process_detail(session, url, films, sem_detail))
            for url in detail_urls
        ]
        await asyncio.gather(*tasks)
        # 保存结果
        with open('films.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(str(film) for film in films))


if __name__ == '__main__':
    asyncio.run(main())

