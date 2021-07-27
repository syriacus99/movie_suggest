import requests
import re
import time
import pandas as pd
import numpy as np
from lxml import etree
# 代理地址
proxy_ip = ""
proxy_port = ""

# 代理设置
proxies = {
    "http": "http://" + proxy_ip + ":" + proxy_port,
    "https": "https://" + proxy_ip + ":" + proxy_port
}

HTML500_RESPONSE = '<!doctype html><html><head><meta charset="utf-8"><title>500</title></head><body><h3>500</h3></body></html>'

class movie_API:
    name = ''
    info = ''
    response = ''
    url_set = set()
    url_list = list()
    def __init__(self):
        pass

    def url_info_get(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Host': 'www.imdb.cn'
        }
        page = 1
        while(self.response != HTML500_RESPONSE):
            url =  'https://www.imdb.cn/movies/?page=' + str(page)
            self.response = requests.get(url=url, headers=headers).text

            for each in re.findall(r"/title/tt\w+",self.response):
                self.url_set.add(each)

            # tree = etree.HTML(response)
            # url_list = tree.xpath('//li/a[@href]')
            # for url_sub in url_list:
            #     print(etree.tostring(url_sub))
            print("successful page ", page)
            print(len(self.url_set))
            page+=1
            time.sleep(0.6)

    def url_get(self):
        return self.url_set

    def get_url_from_file(self):
        with open("b.txt","r") as f:
            #从缓存的文件中读取获取的电影url
            url_Longstring = f.readline()
            self.url_list = url_Longstring.strip('{').strip('}').replace('\'','').split(', ')

    def movie_info_get(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Host': 'www.imdb.cn'
        }
        director=star=movie_type=area=language=premiere_time=''
        director_list = star_list = movie_type_list = area_list = language_list = premiere_time_list = list()
        if self.url_list:
            whole_url_list = list()
            for each_url in self.url_list:
                whole_url_list.append("www.imdb.cn" + each_url)
                for url in whole_url_list:
                    r = requests.get(url, headers=headers).text
                    # a = re.findall(r'<div class="per_txt" fr>(.*)</div><!',r)
                    tree = etree.HTML(r)
                    # 电影名称
                    movie_name = tree.xpath('//div[@class="per_txt fr"]/h1/div/text()')
                    tree.xpath('//div[@class="per_txt fr"]/h1/div/text()')
                    bar_list = tree.xpath('//div[@class="txt_bottom_item"]')
                    for each_bar in bar_list:
                        # message1若非空依次为导演，编剧，主演
                        message1 = each_bar.xpath('.//div[@class="txt_bottom_r txt_bottom_r_overflow"]/a/text()')
                        # message2若非空依次为类型,制片国家/地区,语言,首播时间，季数，单集片长，别名
                        message2 = each_bar.xpath('.//div[@class="txt_bottom_r"]/text()')
                        # message3为获取当前信息是哪一项如：是导演
                        message3 = each_bar.xpath('.//div[@class="txt_bottom_l"]/text()')
                        print(message3)
                        if message1:
                            if message3[0] == '导演：':
                                director = message1
                            elif message3[0] == '主演：':
                                star = message1
                        if message2:
                            if message3[0] == '类型：':
                                movie_type = message2[0].strip()
                            elif message3[0] == '制片国家/地区：':
                                area = movie_type = message2[0].strip()
                            elif message3[0] == '语言：':
                                language = movie_type = message2[0].strip()
                            elif message3[0] == '首播：':
                                premiere_time = movie_type = message2[0].strip()


a = movie_API()
a.get_url_from_file()
a.movie_info_get()
#with open("a.txt","w") as f:
 #   f.write(str(a.url_get()))