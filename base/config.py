import os
from pathlib import Path
from dotenv import load_dotenv
from fake_useragent import UserAgent

class Config:
    def __init__(self):
        # 加载.env文件
        env_path = Path(__file__).parent.parent / '.env'
        load_dotenv(env_path)
        
        # MongoDB配置
        self.mongodb_uri = os.getenv('MONGODB_URI')
        self.mongodb_db = os.getenv('MONGODB_DB')
        
        # Redis配置
        self.redis_host = os.getenv('REDIS_HOST')
        self.redis_port = int(os.getenv('REDIS_PORT', 6379))
        self.redis_db = int(os.getenv('REDIS_DB', 0))
        
        # 代理配置
        self.proxy_enabled = os.getenv('PROXY_ENABLED', 'false').lower() == 'true'
        self.proxy_api_url = os.getenv('PROXY_API_URL')
        self.proxy_username = os.getenv('PROXY_USERNAME')
        self.proxy_password = os.getenv('PROXY_PASSWORD')
        
        # 存储配置
        self.file_storage_enabled = os.getenv('FILE_STORAGE_ENABLED', 'true').lower() == 'true'
        self.file_storage_path = os.getenv('FILE_STORAGE_PATH', './data')
        
        # UA生成器
        self._ua = UserAgent()
    
    @property
    def user_agent(self):
        """获取随机UA"""
        return self._ua.random
    
    def get_proxy(self):
        """获取代理配置"""
        if not self.proxy_enabled:
            return None
            
        # 如果需要，这里可以实现代理池逻辑
        return {
            'http': self.proxy_api_url,
            'https': self.proxy_api_url
        }

# 创建全局配置实例
config = Config()