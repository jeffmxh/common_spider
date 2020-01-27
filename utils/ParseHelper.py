# coding: utf-8

"""
__title__ = 'ParseHelper'
__author__ = 'Jeffmxh'
                   _ooOoo_
                  o8888888o
                  88" . "88
                  (| -_- |)
                  O\  =  /O
               ____/`---'\____
             .'  \\|     |//  `.
            /  \\|||  :  |||//  \
           /  _||||| -:- |||||-  \
           |   | \\\  -  /// |   |
           | \_|  ''\---/''  |   |
           \  .-\__  `-`  ___/-. /
         ___`. .'  /--.--\  `. . __
      ."" '<  `.___\_<|>_/___.'  >'"".
     | | :  `- \`.;`\ _ /`;.`/ - ` : | |
     \  \ `-.   \_ __\ /__ _/   .-` /  /
======`-.____`-.___\_____/___.-`____.-'======
                   `=---='
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            佛祖保佑       永无BUG
"""

import re
import json
from lxml import etree

from spider.utils.DictTools import DictTools
from spider.utils.LoggingUtils import logger
from spider.config.config import spider_config

class ParseHelper:
    domain_pattern = re.compile('|'.join([re.sub(r'\.', '\.', x) for x in spider_config.DOMAIN]))
    @staticmethod
    def parse_url(html_text):
        all_urls = []
        all_urls += ParseHelper.parse_href(html_text)
        all_urls += ParseHelper.parse_json_url(html_text)
        all_urls = [ParseHelper.complete_url(x) for x in all_urls]
        all_urls = [x for x in all_urls if ParseHelper.domain_pattern.search(x)]
        all_urls = list(set(all_urls))
        logger.info('{} urls fetched!'.format(len(all_urls)))
        return all_urls

    @staticmethod
    def parse_root_url(html_text):
        urls = ParseHelper.parse_url(html_text)
        root_urls = [ParseHelper.parse_root(x) for x in urls]
        root_urls = list(set([x for x in root_urls if x]))
        logger.info('{} root urls fetched!'.format(len(root_urls)))
        return root_urls

    @staticmethod
    def parse_root(url):
        match = re.search(r'https://.+?\.com', url)
        if not match:
            logger.warning(f'[URL]: {url} does not match url format')
            return ''
        else:
            return match.group()
    @staticmethod
    def parse_href(html_text):
        if not isinstance(html_text, str):
            logger.warning(f'Povided input has type: {type(html_text)}, not str')
        try:
            return etree.HTML(html_text).xpath('//a/@href')
        except:
            logger.warning('Cannot parse provided text')
            return []

    @staticmethod
    def parse_json(html_text):
        json_data = re.search(r'var allData = (?P<jsondata>[\d\D]+?);', html_text).group('jsondata')
        try:
            data = json.loads(json_data)
            return data
        except:
            logger.warning('Parsing json data failed')
            return {}

    @staticmethod
    def parse_json_url(html_text):
        json_data = ParseHelper.parse_json(html_text)
        if json_data:
            flat_data = DictTools.flatten_dict(json_data)
            urls = [y for x, y in flat_data.items() if x.endswith('_url')]
        else:
            urls = []
        return urls

    @staticmethod
    def complete_url(url):
        if not url.startswith('http'):
            url = 'https:' + url
        url = re.sub(r'http://', 'https://', url)
        url = re.sub(r'/$', '', url)
        url = re.sub(r'#.+?$', '', url)
        return url