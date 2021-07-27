import requests
import re
import time
from lxml import etree
url = "https://www.imdb.cn/title/tt11043632"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Host': 'www.imdb.cn'
}
r = requests.get(url,headers=headers).text
#a = re.findall(r'<div class="per_txt" fr>(.*)</div><!',r)
tree = etree.HTML(r)
#电影名称
movie_name = tree.xpath('//div[@class="per_txt fr"]/h1/div/text()')
tree.xpath('//div[@class="per_txt fr"]/h1/div/text()')
bar_list = tree.xpath('//div[@class="txt_bottom_item"]')
for each_bar in bar_list:
    #message1若非空依次为导演，编剧，主演
    message1 = each_bar.xpath('.//div[@class="txt_bottom_r txt_bottom_r_overflow"]/a/text()')
    #message2若非空依次为类型,制片国家/地区,语言,首播时间，季数，单集片长，别名
    message2 = each_bar.xpath('.//div[@class="txt_bottom_r"]/text()')
    #message3为获取当前信息是哪一项如：是导演
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
print(director,star,movie_type,area,language,premiere_time)