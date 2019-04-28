# SXSpider：用来爬取最高人民法院失信被执行人信息的玩具爬虫

## 系统要求

1. Python3 可以去 [Python官方网站](http://www.python.org) 下载
2. requests 库，安装完python后可以使用命令： *pip install requests* 进行安装
   
## 使用方法

在命令行执行 **python start.py** 即可。返回的结果会保存在 shixin.db 这个 sqlite 数据库中。

## 注意事项

我目前只测试了少量页面，没有全量爬取，不清楚当爬取量很大的时候会不会遇上反爬虫技术。需要全量抓取的筒子请自己修改 start.py 中的循环。
