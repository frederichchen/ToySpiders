import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class SXSpider:
    def __init__(self):
        """ 初始化 ChromeDriver，并写入数据表的表头
        """
        self.driver = webdriver.Chrome()
        self.fout = open('result.txt', 'w')
        self.fout.write(
            '被执行人名称,被执行人证件号码,法人或负责人姓名,执行法院,省份,案号,生效法律文书确定的义务,被执行人的履行情况,失信被执行人行为具体情形,发布时间'
        )
        self.fout.write("\n")

    def __del__(self):
        self.fout.close()
        # self.driver.close()

    def open_page(self):
        """ 访问百度，输入失信被执行人进行搜索
        """
        self.driver.get("http://www.baidu.com")
        time.sleep(3)
        try:
            input = self.driver.find_element_by_id('kw')
            input.send_keys("失信")
            time.sleep(1)
            input.send_keys("被执行人")
            time.sleep(1)
            input.send_keys(Keys.ENTER)
            WebDriverWait(self.driver, 80).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, 'div.op_trust_mainBox')))
        except TimeoutException:
            print("出现问题，百度未能打开相应的页面！")
            sys.exit(1)
        except NoSuchElementException:
            print("百度输入出错！")
            sys.exit(1)

    def fetch_page_data(self):
        """ 爬取单页数据
        """
        items = self.driver.find_elements_by_css_selector('li.op_trust_item')
        for item in items:
            try:
                xm = item.find_element_by_css_selector(
                    'span.op_trust_name').text
                zjhm = item.find_element_by_css_selector(
                    'span.op_trust_fl').text
                # 百度的设置很怪，要点开后才能爬取数据
                ActionChains(self.driver).click(item).perform()
                values = item.find_elements_by_css_selector(
                    'tbody td.op_trust_tdRight')
            except StaleElementReferenceException:
                # 如果出现获取元素失败的问题就休息一秒再度抓取
                try:
                    print("出现异常，等待重试...")
                    time.sleep(1)
                    ActionChains(self.driver).click(item).perform()
                    values = item.find_elements_by_css_selector(
                        'tbody td.op_trust_tdRight')
                except StaleElementReferenceException:
                    print("重试失败，跳过该公告...")
                    continue
            if len(values) == 7:
                self.fout.write(
                    "'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'" %
                    (xm, zjhm, '', values[0].text, values[1].text,
                     values[2].text, values[3].text, values[4].text,
                     values[5].text, values[6].text))
            else:
                self.fout.write(
                    "'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'" %
                    (xm, zjhm, values[0].text, values[1].text, values[2].text,
                     values[3].text, values[4].text, values[5].text,
                     values[6].text, values[7].text))
            self.fout.write("\n")

    def fetch_data(self, maxnum=-1):
        """ 获取数据，参数 maxnum 为获取的页数，如果为 -1 则表示获取所有页面
        """
        pagenum = 1
        print("获取第%d页的数据..." % pagenum)
        self.fetch_page_data()
        while (maxnum == -1 or pagenum < maxnum):
            try:
                next_btn = self.driver.find_element_by_css_selector(
                    'div.op_trust_page span.op_trust_page_next')
                ActionChains(self.driver).click(next_btn).perform()
                time.sleep(2)
                pagenum = pagenum + 1
                print("------------------------")
                print("获取第%d页的数据..." % pagenum)
                self.fetch_page_data()
            except NoSuchElementException:
                return
        print("完成！")


if __name__ == "__main__":
    sp = SXSpider()
    sp.open_page()
    sp.fetch_data(3)
