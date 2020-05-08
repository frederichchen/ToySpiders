# PSASpider：用来爬取国家知识产权局专利检索库数据的玩具爬虫

## 系统要求

1. Python3 可以去 [Python官方网站](http://www.python.org) 下载
2. selenium 库，安装完python后可以使用命令： *pip install selenium* 进行安装
3. 浏览器及相应的 Driver，如果用谷歌浏览器则用 chromedriver，Firefox则用 geckodriver 。
   
## 使用方法

在命令行执行 **python SXSpider.py** 即可。文件的最后一行调用fetch_data的参数为爬取的页数，可以修改，如果留空则爬取所有。

## 注意事项

返回的结果将写入 result.txt 文件，该文件的字段用逗号分隔，文本识别符为单引号。如果需要使用数据库请自行修改。