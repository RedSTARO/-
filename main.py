# coding=utf-8
"""
展示天气图片
"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qt import Qt
from weather_dll import *

class Myweather:
    def __init__(self):
        self.app = QApplication(sys.argv)
        # 创建一个窗体
        self.window = QWidget()
        # 设置窗体位置大小
        self.window.setGeometry(300, 300, 400, 600)
        # 设置标题图标
        self.window.setWindowIcon(QIcon("favicon.ico"))
        # 设置窗体标题
        self.window.setWindowTitle("天气查询系统 By:RedSTAR ")
        # 创建网格布局管理器
        grid = QGridLayout()
        # 设置网格间隔
        grid.setSpacing(10)
        # 网格布局
        self.window.setLayout(grid)

        # 创建标题
        self.lb_search = QLabel('天气查询')
        self.lb_search.setAlignment(Qt.AlignCenter)
        self.lb_search.setFont(QFont("Times", 21))
        grid.addWidget(self.lb_search, 0, 0, 1, 2)

        # 本地信息
        self.lb_city = QLabel("城市：")
        self.lb_city.setAlignment(Qt.AlignCenter)
        self.lb_city.setFont(QFont('Times', 16))
        grid.addWidget(self.lb_city, 1, 0, 1, 1)

        # 城市输入框
        # 自动定位展示
        try:
            import ip
            import re
            spider = ip.Spider()
            auto_space_info = "自动定位：{}".format(str(spider.BeautifulSoup_find())[20:26])
            auto_space = str(spider.BeautifulSoup_find())
            # 自动定位城市
            auto_space = re.sub(r'</span>', "", re.sub(r'<span class="c-red">', "", str(auto_space)))
            for_num_1 = 0
            for i in auto_space:
                for_num_1 += 1
                if i == "省":
                    auto_space = auto_space[for_num_1:]
                if i == "市":
                    auto_space = auto_space[:-4]
        except:
            auto_space_info = "未能自动定位，请手动输入城市"

        self.edit_city = QLineEdit(auto_space)
        # self.edit_city.setPlaceholderText(auto_space_info)
        self.edit_city.setFont(QFont('Times', 16))
        grid.addWidget(self.edit_city, 1, 1, 1, 1)

        # 今日天气
        self.btn_1d = QPushButton('查看今天天气')
        self.btn_1d.setFont(QFont('Times', 13))
        grid.addWidget(self.btn_1d, 2, 0, 1, 1)

        # 7日天气
        self.btn_7d = QPushButton('查看未来7天天气')
        self.btn_7d.setFont(QFont('Times', 13))
        grid.addWidget(self.btn_7d, 2, 1, 1, 1)

        # 展示区
        self.weather_info = QTextBrowser()
        self.weather_info.setText(auto_space_info)
        self.weather_info.setFont(QFont('Times', 13))
        grid.addWidget(self.weather_info, 3, 0, 1, 2)

    # 展示今日的天气
    def set_1d_weather(self):
        text = self.edit_city.text()
        data = ''
        if text:
            ret = spider_1dweather(text)
            if ret:
                for key, val in ret['daytime'].items():
                    if val:
                        data += val + '\n'
                # 夜间
                data += '\n'
                for key, val in ret['night'].items():
                    if val:
                        data += val + '\n'
            else:
                data = "没有找到此城市天气(OneDayNotFound)"
        else:
            data = "请输入城市"
        self.weather_info.setText(data)

    # 展示未来7天天气
    def set_7d_weather(self):
        text = self.edit_city.text()
        data = ''
        if text:
            ret = spider_7dweather(text)
            if ret:
                # data = ""
                for i in range(7):
                    for key, val in ret[str(i)].items():
                        if val:
                            data += val + "\n"
                    data += "\n"
            else:
                data = "没有找到此城市天气(SevenDaysNotFound)"
        else:
            data = "请输入城市"
        self.weather_info.setText(data)

        self.weather_info.setText(data)

    def run(self):
        # 事件绑定
        self.btn_1d.clicked.connect(self.set_1d_weather)
        self.btn_7d.clicked.connect(self.set_7d_weather)
        # 显示窗体
        self.window.show()
        # 退出时清理
        self.app.exec_()


if __name__ == '__main__':
    app = Myweather()
    app.run()
