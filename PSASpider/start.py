#!/usr/bin/python3
from PSASpider import PSASpider


keywords = ['君实生物', '恒成工具', '某个歪公司']
sp = PSASpider()
sp.login()
for k in keywords:
    print("查询%s" % k)
    res = sp.make_query(k)
    print(res)
sp.exit()
