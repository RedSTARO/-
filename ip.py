import requests
from bs4 import BeautifulSoup


# 定义爬虫类
class Spider():
    def __init__(self):
        self.url = 'http://mip.chinaz.com/'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        r = requests.get(self.url,headers=self.headers)
        r.encoding = r.apparent_encoding
        self.html = r.text

    def BeautifulSoup_find(self):
        # < span class ="c-red" > 安徽省合肥市 电信 < / span >
        soup = BeautifulSoup(self.html, 'lxml')   # 转换为BeautifulSoup的解析对象()里第二个参数为解析方式
        titles = soup.find_all('span', class_="c-red")
        return titles[2]
        # print(titles[2], titles[1])



if __name__ == '__main__':
    spider = Spider()
    spider.BeautifulSoup_find()
