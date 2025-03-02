from abc import ABC, abstractmethod
from lxml import etree
from jsonpath import jsonpath
import json

class BaseParser(ABC):
    """解析器基类"""
    @abstractmethod
    def parse(self, content):
        """解析方法"""
        pass

class XPathParser(BaseParser):
    """XPath解析器"""
    def __init__(self, rules):
        """
        初始化XPath解析器
        :param rules: XPath规则字典，格式为 {字段名: xpath表达式}
        """
        self.rules = rules
        
    def parse(self, content):
        """使用XPath解析HTML内容"""
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        html = etree.HTML(content)
        result = {}
        
        for field, xpath in self.rules.items():
            values = html.xpath(xpath)
            if values:
                # 如果只有一个值，直接保存；否则保存为列表
                result[field] = values[0] if len(values) == 1 else values
                
        return result

class JSONPathParser(BaseParser):
    """JSONPath解析器"""
    def __init__(self, rules):
        """
        初始化JSONPath解析器
        :param rules: JSONPath规则字典，格式为 {字段名: jsonpath表达式}
        """
        self.rules = rules
        
    def parse(self, content):
        """使用JSONPath解析JSON内容"""
        if isinstance(content, str):
            content_json = json.loads(content)
            
        result = {}
        for field, jsonpath_rule in self.rules.items():
            print(field, jsonpath_rule)
            matches = jsonpath(content_json, jsonpath_rule)
            if matches:
                result[field] = matches[0] if len(matches) == 1 else matches
                
        return result

def create_parser(parser_type='xpath', rules=None):
    """解析器工厂方法"""
    if rules is None:
        rules = {}
        
    parsers = {
        'xpath': XPathParser,
        'jsonpath': JSONPathParser
    }
    return parsers.get(parser_type, XPathParser)(rules)