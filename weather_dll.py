# # coding=utf-8
# # 天气查询系统爬取网络的扩展
import requests
from bs4 import BeautifulSoup


def get_city_id(city):
    url = "http://toy1.weather.com.cn/search"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"
                      " (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36"
    }
    params = {
        "cityname" : city
    }
    response = requests.get(url, headers=header, params=params)
    citys = response.content.decode("utf-8")
    if city in citys:
        start = citys.find(":")
        end = citys.find("~")
        cityid = citys[start + 2:end]
    else:
        cityid = False
    return cityid

# 获取当日天气信息
def spider_1dweather(city):
    cityid = get_city_id(city)
    if cityid:
        url = "http://www.weather.com.cn/weather1d/" + str(cityid) + ".shtml"
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }

        response = requests.get(url, headers=header)
        html = response.content.decode("utf-8")
        soup = BeautifulSoup(html, 'lxml')

        weather_info = {
            "title": None,
            "wea": None,
            "tem": None,
            "win": None,
            "sun": None
        }

        # 今日天气
        weather = {
            "daytime": weather_info,
            "night": weather_info.copy()
        }

        # 定义到class属性值为"t"的div标签
        div_tag = soup.find_all("div", attrs={"class": "t"})[0]
        # 抓取白天的天气
        # 标题
        weather['daytime']['title'] = div_tag.find_all("h1")[0].get_text()
        # 天气
        weather['daytime']['wea'] = "天气：" + soup.find_all("p", attrs={"class": "wea"})[0].get_text()
        # 温度
        weather['daytime']['tem'] = "温度：" + div_tag.find_all("p", attrs={"class": "tem"})[0].get_text().replace("\n", "")
        # 风速
        weather['daytime']['win'] = "风速：" + div_tag.find_all("p", attrs={"class": "win"})[0].get_text().replace("\n", "")
        # 日落时间
        weather['daytime']['sun'] = div_tag.find_all("p", attrs={"class": "sun"})[0].get_text().replace("\n", "")

        # 抓取夜间天气
        # 标题
        weather['night']['title'] =div_tag.find_all("h1")[1].get_text()
        # 天气
        weather['night']['wea'] = "天气：" + div_tag.find_all("p", attrs={"class": "wea"})[1].get_text()
        # 温度
        weather['night']['tem'] = "温度：" + div_tag.find_all("p", attrs={"class": "tem"})[1].get_text().replace("\n", "")
        # 风速
        weather['night']['win'] = "风速：" + div_tag.find_all("p", attrs={"class": "win"})[1].get_text().replace("\n", "")
        # 日落时间
        weather['night']['sun'] =div_tag.find_all("p", attrs={"class": "sun"})[1].get_text().replace("\n", "")
        return weather
    else:
        return False


# 获取未来7日的天气信息
def spider_7dweather(city):
    cityid = get_city_id(city)
    if cityid:
        url = "http://www.weather.com.cn/weather/" + str(cityid) + ".shtml"
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"
                        " (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36"
        }

        response = requests.get(url, headers=header)
        html = response.content.decode("utf-8")
        soup = BeautifulSoup(html, 'lxml')

        weather_info = {
            "title": None,
            "wea": None,
            "tem": None,
            "win": None,
        }
        # 7日天气
        weather = dict()
        for i in range(7):
            weather[str(i)] = weather_info.copy()

        ul_tag = soup.find_all("ul", attrs={"class": "t clearfix"})[0]
        for i in range(7):
            li_tag = ul_tag.find_all("li")[i]
            # 标题
            weather[str(i)]['title'] = li_tag.h1.get_text()
            # 天气
            weather[str(i)]['wea'] = "天气："+li_tag.find_all("p")[0].get_text()
            # 风速
            weather[str(i)]['win'] = "最高/低温：" + li_tag.find_all("p")[1].get_text().replace("\n", "")
            # 温度上限
            weather[str(i)]['tem'] = "风速："+ li_tag.find_all("p")[2].get_text().replace("\n", "")
        return weather
    else:
        return False

"""

# 获取天气预报视频
def spider_1dweather(city):
    cityid = get_city_id(city)
    if cityid:# https://vod.weathertv.cn/video/2020/10/29/202010301604059202407_1_1520.mp4

    else:
        return False
        
"""
