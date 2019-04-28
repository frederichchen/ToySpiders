#!/usr/bin/python3
import requests
from random import choice
from agents import AGENTS_ALL


class SXSpider:
    """ SXSpider 类，爬取失信被执行人数据
    Attributes:
        api_url      字符串类型，百度API的网址
        params       字典类型，需要传入API的参数
        headers      字典类型，请求的头信息
    """

    def __init__(self):
        self.api_url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php'
        self.params = {
            'resource_id': 6899,
            'query': '失信被执行人',
            'pn': 0,
            'rn': 10,
            'ie': 'utf-8',
            'oe': 'utf-8',
            'format': 'json',
        }
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'sp0.baidu.com',
            'User-Agent': choice(AGENTS_ALL),
            'Referer': 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E5%A4%B1%E4%BF%A1%E8%A2%AB%E6%89%A7%E8%A1%8C%E4%BA%BA&rsv_pq=9e51480100012da5&rsv_t=599bNSH5yr0PGC8glIQTIVpMLW6OEVOs3996IDd9DiQnuThTLfg84gJ11A0&rqlang=cn&rsv_enter=1&rsv_sug3=2&rsv_sug1=2&rsv_sug7=100'
        }

    def get_data(self, page):
        """ 获取相应数据并返回
        Args:
            page    整型，表示也数，因为网页对数据进行了分页处理

        Return:
            bulletins  列表类型，包含了失信被执行人相关数据
        """
        self.params['pn'] = page * 10
        try:
            response = requests.get(self.api_url,
                                    headers=self.headers,
                                    params=self.params)
            bulletins = response.json()['data'][0]['result']
        except Exception as e:
            print(e)
            return []
        else:
            return bulletins

