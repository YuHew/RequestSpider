import re
from bs4 import BeautifulSoup

from base.downloader import *
from base.parser import *
from base.storage import *




def static_xpath_file():
    downloader = create_downloader()
    response = downloader.download('https://www.baidu.com')

    parse_xpath = create_parser(rules={'content':'/html/head/meta[5]/@content'})
    result = parse_xpath.parse(response.text)
    for field, title in result.items():
        print(field, title)

    storage = create_storage(storage_type = 'file', folder_name = 'baidu')
    storage.save(result['content'])


def static_json_file():
    downloader = create_downloader('api')
    response = downloader.download('https://api.it8.com.cn/juejin/')

    parse_json = create_parser('jsonpath', rules={'title': '$..title'})
    result = parse_json.parse(response.text)
    for field, title in result.items():
        print(field, title)

    storage = create_storage(storage_type='file', folder_name='api')
    storage.save(result)

def douyin_demo():
    downloader = create_downloader()
    response = downloader.download('https://v.douyin.com/i5QkfYov/', allow_redirects=False)

    if response.status_code in (301, 302, 303, 307, 308):
        redirected_url = response.next.url
        print(redirected_url)
        match = re.search(r'/video/(\d+)/', redirected_url)
        if match:
            return match.group(1).strip()


def douyin_video_info(video_id):
    downloader = create_downloader()
    url = f'https://www.douyin.com/aweme/v1/play/?ratio=1080p&video_id={video_id}'
    print(url)
    response = downloader.download(url, allow_redirects=False)
    print(response.status_code)
    print(response.text)

def fix_extra_braces_advanced(text: str) -> str:
    """
    使用栈结构精确修复嵌套层级问题
    示例：
    输入：'{{"name": "John"} } }'
    输出：'{"name": "John"}'
    """
    stack = []
    clean = []
    skip_next = False

    for i, char in enumerate(text):
        if char == '{':
            stack.append(char)
            clean.append(char)
        elif char == '}':
            if stack and stack[-1] == '{':
                stack.pop()
                clean.append(char)
            else:
                # 忽略多余闭合括号
                continue
        else:
            clean.append(char)

    # 补全未闭合的括号
    while stack:
        clean.append('}')
        stack.pop()

    return ''.join(clean)

def extract_router_data(url: str) -> str:

    downloader = create_downloader()
    response = downloader.download('https://v.douyin.com/i5QkfYov/')
    print(response.status_code)
    print(response.text)

    soup = BeautifulSoup(response.text, 'html.parser')
    body_tag = soup.body
    if not body_tag:
        print("未找到 <body> 标签")
        return {}
    # 3. 在 body 中查找所有 script 标签
    json_data = {}
    pattern = re.compile(
        r'window\._ROUTER_DATA\s*=\s*({.*?})\s*;?',
        re.DOTALL  # 允许匹配换行符
    )
    for script in body_tag.find_all('script'):
        script_text = script.string
        if not script_text or "window._ROUTER_DATA" not in script_text:
            continue
        print("找到window._ROUTER_DATA")
        # 4. 使用正则提取 JSON
        match = pattern.search(script_text)
        if match:
            print("找到window._ROUTER_DATA并且match")
            json_str = match.group(1)
            try:
                # 处理 Unicode 转义字符（如 \u002F）
                json_str = fix_extra_braces_advanced(json_str)
                print(json_str)
                json_data = json.loads(json_str)
                break  # 找到后立即退出
            except json.JSONDecodeError as e:
                print(f"JSON 解析失败: {e}")
                continue

    print(f'json_data + {json_data}')

    return json_data


if __name__ == '__main__':
    # print(extract_router_data('https://v.douyin.com/i5QkfYov/'))
    # item_id = douyin_demo()
    # douyin_video_info(item_id)
    # static_json_file()
    static_xpath_file()


