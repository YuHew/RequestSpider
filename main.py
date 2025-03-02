
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


if __name__ == '__main__':
    static_json_file()
    static_xpath_file()

