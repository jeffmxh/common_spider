# coding: utf-8

"""
__title__ = 'DictTools'
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

class DictTools:
    '''
    用于将多层嵌套字典打平
    :params adict: 待处理的字典
    :returns: 打平后字典
    :usage:
    >>> adict = {'name': 'ipuyu', 'education': {'school': 'nju', 'graduation': '2020'}}
    >>> DictTools.flatten_dict(adict)
    ## {'name': 'ipuyu', 'education_school': 'nju', 'education_graduation': '2020'}
    '''
    @staticmethod
    def flatten_dict(adict):
        copy = __import__('copy')
        temp = copy.deepcopy(adict)
        while isinstance(temp, dict) and any(isinstance(v, (list, tuple, dict)) for k, v in temp.items()):
            temp = DictTools._flatten_dict(temp)
        return temp

    @staticmethod
    def _flatten_dict(adict):
        result = {}
        for k, v in adict.items():
            if isinstance(v, dict):
                for kk, vv in v.items():
                    kk_re = DictTools.trans_name(kk)
                    key_name = '{}_{}'.format(k, kk_re)
                    result[key_name] = vv
            elif isinstance(v, (list, tuple)):
                for i, x in enumerate(v):
                    key_name = '{}_{}'.format(k, i)
                    result[key_name] = x
            else:
                result[k] = v
        return result

    @staticmethod
    def trans_name(key_name):
        '''
        转化包含_的Key
        '''
        re = __import__('re')
        if re.search('_', key_name):
            key_list = re.split('_+', key_name)
            key_list = [x.title() for x in key_list]
            key_name = ''.join(key_list)
        return key_name

if __name__ == '__main__':
    adict = {
        'a': {
            'a1': 'aaa',
            'a2': 'aaaaa'
        },
        'b': [
            {'key': 1},
            {'key': 2},
            {'key': 3}
        ]
    }

    print(DictTools.flatten_dict(adict))