from abc import ABC, abstractmethod
import requests
import selenium
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome.options import Options
# import js2py
from base.config import config

class BaseDownloader(ABC):
    """下载器基类"""
    @abstractmethod
    def download(self, url, **kwargs):
        """下载方法"""
        pass

class StaticDownloader(BaseDownloader):
    """静态页面下载器"""
    def download(self, url, **kwargs):
        headers = kwargs.get('headers', {})
        if 'User-Agent' not in headers:
            headers['User-Agent'] = config.user_agent
            
        proxies = kwargs.get('proxies', config.get_proxy())
        timeout = kwargs.get('timeout', 30)
        
        response = requests.get(
            url,
            headers=headers,
            proxies=proxies,
            timeout=timeout,
            **{k:v for k,v in kwargs.items() if k not in ['headers', 'proxies', 'timeout']}
        )
        response.raise_for_status()
        return response

class APIDownloader(BaseDownloader):
    """API接口下载器"""
    def download(self, url, **kwargs):
        method = kwargs.pop('method', 'GET')
        headers = kwargs.get('headers', {})
        if 'User-Agent' not in headers:
            headers['User-Agent'] = config.user_agent
            
        proxies = kwargs.get('proxies', config.get_proxy())
        timeout = kwargs.get('timeout', 30)
        
        response = requests.request(
            method,
            url,
            headers=headers,
            proxies=proxies,
            timeout=timeout,
            **{k:v for k,v in kwargs.items() if k not in ['headers', 'proxies', 'timeout']}
        )
        try:
            response.raise_for_status()
        except Exception as e:
            print(e)
        return response

class DynamicDownloader(BaseDownloader):
    """动态渲染下载器"""
    def __init__(self, use_selenium=True):
        self.use_selenium = use_selenium
        self._driver = None
        
    @property
    def driver(self):
        if self._driver is None and self.use_selenium:
            options = Options()
            options.add_argument('--headless')
            options.add_argument(f'user-agent={config.user_agent}')
            if config.proxy_enabled and config.proxy_api_url:
                options.add_argument(f'--proxy-server={config.proxy_api_url}')
            self._driver = webdriver.Chrome(options=options)
        return self._driver
        
    def download(self, url, **kwargs):
        if self.use_selenium:
            self.driver.get(url)
            return self.driver.page_source
        else:
            # 使用js2py进行渲染
            # response = requests.get(url)
            # context = js2py.EvalJs()
            # context.execute(response.text)
            # return str(context)
            return None
            
    def __del__(self):
        if self._driver:
            self._driver.quit()

def create_downloader(downloader_type='static'):
    """下载器工厂方法"""
    downloaders = {
        'static': StaticDownloader,
        'api': APIDownloader,
        'dynamic': DynamicDownloader
    }
    return downloaders.get(downloader_type, StaticDownloader)()