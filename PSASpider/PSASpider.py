#!/usr/bin/python3
import time
import pickle
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class PSASpider:
    """ PSASpider 类，爬取国家知识产权局专利检索库数据
        网址是： http://www.pss-system.gov.cn/
        由于该网站必须登录后才能查询，因此这个程序是半自动化的，需要用户先登录。
    Attributes:
        driver   用于设置爬取的浏览器自动化程序，我这里用 chromedriver
    """

    def __init__(self):
        self.driver = webdriver.Chrome()

    def login(self):
        """ 访问登录页面，让用户手动登录，并保存 cookie
        """
        self.driver.get(
            "http://www.pss-system.gov.cn/sipopublicsearch/portal/uilogin-forwardLogin.shtml"
        )
        time.sleep(20)
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))

    def make_query(self, keyword):
        """ 输入关键字，爬取查询结果
        Args:
            keyword    字符串类型，表示查询关键字
        Raises:
            NoSuchElementException    selenium没有找到相应的元素
            TimeoutException          等待超时异常
        Return:
            results    列表类型，其中每个元素都是一个dict，包含相应信息
        """
        self.driver.get(
            "http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/searchHomeIndex-searchHomeIndex.shtml"
        )
        # 装载之前登录后获取的 cookie
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            cookie_dict = {
                "domain": cookie.get('domain'),
                'name': cookie.get('name'),
                'value': cookie.get('value'),
                "expires": "",
                'path': cookie.get('path'),
                'httpOnly': cookie.get('httpOnly'),
                'HostOnly': False,
                'Secure': cookie.get('Secure')
            }
            self.driver.add_cookie(cookie_dict)
        # 输入查询关键字，并等待查询结果
        input = self.driver.find_element_by_id('search_input')
        input.send_keys(keyword)
        input.send_keys(Keys.ENTER)
        WebDriverWait(self.driver, 80).until(
            EC.visibility_of_element_located((By.ID, 'search_result_former')))
        results = []
        try:
            patents = self.driver.find_elements_by_css_selector('li.patent')
        except NoSuchElementException:
            return []
        while True:
            for p in patents:
                result = {}
                result['专利名称'] = p.find_element_by_css_selector(
                    'div.item-header h1').text
                info_items = p.find_elements_by_css_selector(
                    'div.item-content-body p')
                for item in info_items:
                    info = item.text.split(':', 1)
                    item_name = re.sub(r'\s+', '', info[0])
                    item_value = re.sub(r'\s+', '', info[1])
                    result[item_name] = item_value
                results.append(result)
            # 将滚动条滚动到窗口最下方
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight)")
            try:
                self.driver.find_element_by_link_text(u'下一页')
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.LINK_TEXT, u'下一页'))).click()
                WebDriverWait(self.driver, 80).until(
                    EC.visibility_of_element_located(
                        (By.ID, 'search_result_former')))
                time.sleep(1)
                patents = self.driver.find_elements_by_css_selector(
                    'li.patent')
            except (NoSuchElementException, TimeoutException):
                return results

    def exit(self):
        """ 关闭浏览器窗口
        """
        self.driver.close()
