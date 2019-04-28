#!/usr/bin/python3
import sqlite3
import time
from SXSpider import SXSpider

conn = sqlite3.connect('shixin.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS SHIXIN
       (省份 TEXT, 被执行人名称 TEXT, 被执行人证件号码 TEXT,
        法人或负责人姓名 TEXT, 案号 TEXT, 执行法院 TEXT, 生效法律文书确定的义务 TEXT,
        被执行人的履行情况 TEXT, 失信被执行人行为具体情形 TEXT, 发布时间 TEXT);''')

sp = SXSpider()
# 这里我只取3页，需要的筒子请改成自己需要的循环
for i in range(3):
    bulletins = sp.get_data(i)
    if bulletins:
        for b in bulletins:
            c.execute(
                "INSERT INTO SHIXIN VALUES (?,?,?,?,?,?,?,?,?,?)",
                (b['areaName'], b['iname'], b['cardNum'], b['businessEntity'],
                 b['caseCode'], b['courtName'], b['duty'], b['performance'],
                 b['disruptTypeName'], b['publishDate']))
    time.sleep(3)

c.close()
conn.commit()
conn.close()
