# PSASpider：用来爬取国家知识产权局专利检索库数据的玩具爬虫

## 系统要求

1. Python3 可以去 [Python官方网站](http://www.python.org) 下载
2. selenium 库，安装完python后可以使用命令： *pip install selenium* 进行安装
3. 浏览器及相应的 Driver，如果用谷歌浏览器则用 chromedriver，Firefox则用 geckodriver 。
   
## 使用方法

在命令行执行 **python start.py** 即可。start.py 中有一个 keywords 列表，可以自己修改。

## 注意事项

目前返回的结果仅仅是 Python 的列表，没有相应的存储。如果需要的话请自己加入存储功能。