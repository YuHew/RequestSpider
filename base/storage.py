from abc import ABC, abstractmethod
import os
import json
from datetime import datetime
from pathlib import Path
from pymongo import MongoClient
from .config import config

class BaseStorage(ABC):
    """存储基类"""
    @abstractmethod
    def save(self, data, **kwargs):
        """保存数据方法"""
        pass

class MongoDBStorage(BaseStorage):
    """MongoDB存储"""
    def __init__(self, collection_name):
        self.client = MongoClient(config.mongodb_uri)
        self.db = self.client[config.mongodb_db]
        self.collection = self.db[collection_name]
        
    def save(self, data, **kwargs):
        """保存到MongoDB"""
        if isinstance(data, list):
            # 批量插入
            self.collection.insert_many(data)
        else:
            # 单条插入
            self.collection.insert_one(data)
            
    def __del__(self):
        if hasattr(self, 'client'):
            self.client.close()

class FileStorage(BaseStorage):
    """文件存储"""
    def __init__(self, folder_name):
        if not config.file_storage_enabled:
            raise ValueError('文件存储功能未启用')
            
        self.storage_dir = Path(config.file_storage_path) / folder_name
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
    def save(self, data, **kwargs):
        """保存到文件"""
        filename = kwargs.get('filename')
        if not filename:
            # 使用时间戳作为文件名
            filename = f'{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            
        file_path = self.storage_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

def create_storage(storage_type='file', **kwargs):
    """存储工厂方法"""
    storages = {
        'mongodb': MongoDBStorage,
        'file': FileStorage
    }
    
    storage_class = storages.get(storage_type)
    if not storage_class:
        raise ValueError(f'不支持的存储类型：{storage_type}')
        
    return storage_class(**kwargs)