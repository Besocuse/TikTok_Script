"""
@author  : AStateoftrance
@time    : 2024/01/16 15:16:21
@function: 抖音自动脚本
@version : 1.0 Beta
"""
from sys import exit
from time import sleep

from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class Script:
    def __init__(self, browser: str):
        if browser == 'edge':
            self.option = webdriver.EdgeOptions()
            self.option.use_chromium = True
            self.option.add_argument('--ignore-certificate-errors')
            self.driver = webdriver.Edge(options=self.option)
        if browser == 'chrome':
            self.option = webdriver.ChromeOptions()
            self.option.add_argument('--ignore-certificate-errors')
            self.driver = webdriver.Chrome(options=self.option)
        if browser == 'firefox':
            self.option = webdriver.FirefoxOptions()
            self.option.accept_insecure_certs = True
            self.driver = webdriver.Firefox(options=self.option)
        self.comment_filter = Filter()
        self.driver.get('https://www.douyin.com/discover')

    def report_comment(self):
        try:
            sleep(7.5)
            print("----载入完成----")
            while True:
                self.block()
                while True:
                    comment_list = self.driver.find_elements(By.CLASS_NAME, 'sU2yAQQU')
                    temp_list = self.driver.find_elements(By.CLASS_NAME, 'EyX_ij5b')
                    ActionChains(self.driver) \
                        .move_to_element(comment_list[-1]) \
                        .move_by_offset(0, 10) \
                        .perform()
                    sleep(0.3)
                    if self.is_element_present(By.CLASS_NAME, 'fanRMYie'):
                        break
                for index, comment in enumerate(comment_list):
                    if self.comment_filter.has_dirty_words(comment.text):
                        ActionChains(self.driver).move_to_element(temp_list[index]).perform()
                        sleep(0.3)

                        # 等待并移动到[举报评论]并点击
                        element1 = WebDriverWait(self.driver, 8, 0.3).until(
                            lambda x: x.find_element(By.CLASS_NAME, 'DKz96wj3')
                        )
                        ActionChains(self.driver).move_to_element(element1).click().perform()
                        sleep(0.3)

                        # 等待并移动到[谩骂攻击]并点击
                        element2 = WebDriverWait(self.driver, 8, 0.3).until(
                            lambda x: x.find_element(By.CLASS_NAME, 'WPxNO927')
                        )
                        ActionChains(self.driver).move_to_element(element2).click().perform()
                        sleep(0.3)

                        # 移动到最后一个元素并点击
                        element3 = self.driver.find_element(By.CLASS_NAME, '_CNTFYxW')
                        ActionChains(self.driver).move_to_element(element3).click().perform()
                        sleep(0.3)

                        print(f'{index}\t{comment.text}\n')
                comment_list.clear()
        except NoSuchElementException as e:
            print(e.msg)
            print('运行失败，请检查是否正确打开评论区')
        except TimeoutException as e:
            print(e.msg)
            print('运行失败，请检查网络是否通畅')

    def is_element_present(self, by, value) -> bool:
        """
        检查元素是否存在
        :param by: css选择方式
        :param value: 选择器的值
        :return: 如果存在返回True，否则返回False
        """
        try:
            self.driver.find_element(by=by, value=value)
            return True
        except NoSuchElementException:
            return False

    def block(self):
        """
        阻塞进程，直到用户选择操作
        :return: None
        """
        while True:
            print("\n///////////////////")
            op = input("\n输入c运行脚本，输入a添加关键字，输入h获取使用帮助，输入q退出:\n").strip().lower()
            if op == 'c':
                return
            elif op == 'h':
                with open('使用说明.txt', 'r', encoding='utf-8') as ins:
                    for line in ins.readlines():
                        print(line)
            elif op == 'a':
                self.comment_filter.add_dirty_words(input("输入关键字，用空格分割："))
            elif op == 'q':
                exit(0)
            else:
                print('请输入正确的操作符！')


class Filter:

    def __init__(self, dataset_path="prop/douyin_comment2.txt"):
        self.dirty_words = self.load_dirty_words(dataset_path)

    def set_dirty_words(self, dirty_words):
        self.dirty_words = dirty_words

    @staticmethod
    def load_dirty_words(file_path) -> list:
        with open(file_path, 'r', encoding='utf-8') as df:
            dirty_words = [line.strip() for line in df.readlines() if line.strip() != '']
        return dirty_words

    def has_dirty_words(self, text):
        if text is None or len(text.strip()) == 0:
            return False
        for word in self.dirty_words:
            if word in text:
                return True
        return False

    def add_dirty_words(self, words: str):
        self.dirty_words.extend(words)
        with open('prop/douyin_comment2.txt', 'a', encoding='utf-8') as df:
            for word in [_ for _ in words.split(' ')]:
                df.write(word)
                df.write('\n')
                print(f'已添加关键字{word}')

    def del_dirty_words(self, words: str):
        pass


if __name__ == '__main__':
    with open('prop/driver.txt', 'r', encoding='utf-8') as f:
        driver = f.readline().lower()
    Script(driver).report_comment()
