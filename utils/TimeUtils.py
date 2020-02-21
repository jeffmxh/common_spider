# coding: utf-8

"""
__title__ = 'TimeUtils'
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

import time

from functools import wraps
from random import random
from spider.config.config import spider_config
from spider.utils.LoggingUtils import logger

class TimeUtils:
    @staticmethod
    def sleep(**kwargs):
        if kwargs.get('time'):
            time_interval = kwargs['time']
            logger.info(f'Sleeping for {time_interval}s')
        else:
            time_interval = spider_config.TIME_INTERVAL * TimeUtils.random_ratio()
        time.sleep(time_interval)

    @staticmethod
    def random_ratio():
        return random() * spider_config.TIME_RANGE * 2 - spider_config.TIME_RANGE + 1

def lazy_exec(func):
    '''保持间隔执行函数的装饰器'''
    @wraps(func)
    def lazy_func(*args, **kwargs):
        TimeUtils.sleep()
        return func(*args, **kwargs)
    return lazy_func