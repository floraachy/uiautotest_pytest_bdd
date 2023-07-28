# -*- coding: utf-8 -*-
# @Time    : 2021/8/14 12:24
# @Author  : Flora.Chen
# @File    : basepage.py
# @Software: PyCharm
# @Desc: UI自动化测试的一些基础浏览器操作方法

# 标准库导入
import os
# 第三方库导入
import time
from loguru import logger
import pyautogui
from pywinauto.keyboard import send_keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    """
    UI自动化基础操作封装
    """

    def __init__(self, driver):
        self.driver = driver

    def visit(self, url: str):
        """
        访问页面
        :param url:
        :return:
        """
        self.driver.get(url)

    def refresh(self):
        """刷新网页"""
        self.driver.refresh()

    def get_current_url(self):
        """
        获取当前浏览器驱动的地址
        """
        return self.driver.current_url

    def click(self, locator: tuple, force=False):
        """
        鼠标点击，当元素不可点击的时候，使用强制点击
        :param locator: 元素定位，元祖类型
        :param force: 强制点击，默认false
        :return: self
        """
        try:
            elem = self.driver.find_element(*locator)
            if not force:
                self.driver.execute_script("arguments[0].click()", elem)
            else:
                self.driver.execute_script("arguments[0].click({force: true})", elem)
        except Exception as e:
            print("未找到元素:{}".format(e))
            raise e

    def input(self, locator: tuple, text):
        """
        输入内容
        :param locator: 元素定位，元祖类型
        :param text: 输入的内容
        :return: self
        """
        try:
            elem = self.driver.find_element(*locator)
            elem.clear()  # 清空输入框中的文本内容
            time.sleep(1)
            elem.send_keys(text)
            return self
        except NoSuchElementException as e:
            print("未找到元素:{}".format(e))
            raise e

    def wait_element_visibility(self, locator: tuple, timeout=20, poll_frequency=0.2):
        """
        显性等待: 等待元素可见
        :param locator: 元素定位，元祖类型
        :return:
        """
        return WebDriverWait(self.driver, timeout, poll_frequency).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_element_clickable(self, locator: tuple, timeout=10, poll_frequency=0.2):
        """
        显性等待： 等待元素可点击
        :param locator: 元素定位，元祖类型
        :return:
        """
        return WebDriverWait(self.driver, timeout, poll_frequency).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_element_presence(self, locator: tuple, timeout=10, poll_frequency=0.2):
        """
        显性等待： 等待元素被加载出来
        :param locator: 元素定位，元祖类型
        :return:
        """
        return WebDriverWait(self.driver, timeout, poll_frequency).until(
            EC.presence_of_all_elements_located(locator)
        )

    def get_element_attribute(self, locator: tuple, attr_name):
        """
        获取元素属性值
        :param locator: 元素定位，元祖类型
        :return: 元素属性值
        """
        try:
            return self.driver.find_element(*locator).get_attribute(attr_name)
        except NoSuchElementException as e:
            print("未找到元素:{}".format(e))
            raise e

    def get_name(self, locator: tuple):
        """
        获取元素的name属性值
        """
        return self.get_element_attribute(locator, "name")

    def get_title(self, locator: tuple):
        """
        获取元素的title属性值
        """
        return self.get_element_attribute(locator, "title")

    def get_class(self, locator: tuple):
        """
        获取元素的class属性值
        """
        return self.get_element_attribute(locator, "class")

    def switch_to_frame(self, reference=None, timeout=10, poll=0.2):
        """
        iframe切换
        :param reference: 可以是id, name,索引或者元素定位（元祖）
        :param timeout:
        :param poll:
        :return:
        """
        if not reference:
            return self.driver.switch_to.default_content()
        return WebDriverWait(self.driver, timeout, poll).until(
            EC.frame_to_be_available_and_switch_to_it(reference)
        )

    def switch_new_window(self):
        """切换到新窗口"""
        # 获取所有的窗口
        windows = self.driver.window_handles
        if len(windows) >= 2:
            # 切换窗口
            self.driver.switch_to.window(self.driver.window_handles[-1])
        return self

    def find_elements(self, locator):
        """
        查找元素们
        :param locator:
        :return:
        """
        try:
            logger.debug(f"正在定位页面的: {locator} 的元素")
            print(f"正在定位页面的: {locator} 的元素")
            element_list = self.driver.find_elements(*locator)
            return element_list
        except NoSuchElementException as e:
            logger.error(f"页面定位元素:{locator}定位失败, 错误信息：{e}")
            print(f"页面定位元素:{locator}定位失败, 错误信息：{e}")
            raise e

    def get_text(self, locator: tuple):
        """
        获取元素的文本值
        :param locator: 元素定位
        :return:
        """
        try:
            elem = self.driver.find_element(*locator)
            value = elem.text
            return value
        except NoSuchElementException as e:
            print(f"get未找到元素{e}")
            raise e

    def screenshot(self, path, filename):
        """
         截图
        :param path: 文件保存的目录
        :param filename: 截图文件名
        :return:
        """
        file_path = os.path.join(path, filename)
        self.driver.save_screenshot(file_path)
        return self

    # ------------------------ START: JS事件 ------------------------ #
    def execute_js(self, js, *args):
        """
        执行javascript脚本
        js: 元组形式参数
        """
        self.driver.execute_script(js, *args)
        return self

    def new_open_window(self, url):
        """打开一个新窗口"""
        # 获取所有的窗口
        start_window = self.driver.window_handls
        # 打开新窗口
        js = "window.open({})".format(url)
        self.driver.execute_script(js)
        # 等待新窗口出现，进行切换
        WebDriverWait(self.driver, 5, 0.5).until(
            EC.new_window_is_opened(start_window)
        )
        # 切换窗口
        self.driver.switch_to.window(self.driver.window_handls[-1])
        return self

    def upload_file_pywinauto(self, file_path):
        """
        使用pywinauto来上传
            缺点：只能在windows上使用。
            优点：可以选择多个文件，路径中有中文也可以。
            安装：pip install pywinauto -i https://mirrors.aliyun.com/pypi/simple/
        ：param file_path: 文件绝对路径,支持传数组
        """
        if isinstance(file_path, list):
            for path in file_path:
                # 上传文件
                send_keys(path)
        else:
            # 上传文件
            send_keys(file_path)
        # 点击回车
        send_keys("{VK_RETURN}")
        return self

    def upload_file_pyautogui(self, file_path):
        """
        使用pyautogui来上传
            缺点：只能选择一个文件，路径中有中文会出问题。
            优点：跨平台。Linux, mac，windows都可以。
            安装：pip install pyautogui -i https://mirrors.aliyun.com/pypi/simple/
        ：param file_path: 文件绝对路径,支持传数组
        """
        if isinstance(file_path, list):
            print("只能选择一个文件，默认选择第一个")
            file_path = file_path[0]

        # 上传文件
        pyautogui.write(file_path)
        # 点击回车
        pyautogui.press("enter", 2)
        return self

    # ------------------------ END: JS事件 ------------------------ #

    # ------------------------ START: 鼠标事件：双击，悬停，拖动 ------------------------ #

    def double_click(self, locator):
        """
        鼠标双击
        :param locator:
        :return:
        """
        try:
            elem = self.driver.find_element(*locator)
            action = ActionChains(self.driver)
            action.double_click(elem).perform()
            return self
        except NoSuchElementException as e:
            print("未找到元素:{}".format(e))
            raise e

    def drag_and_drop(self, start_locator, end_locator):
        """鼠标拖动"""
        elem_start = self.driver.find_element(*start_locator)
        elem_end = self.driver.find_element(*end_locator)
        action = ActionChains(self.driver)
        action.double_click((elem_start, elem_end)).perform()
        return self

    def hover(self, locator):
        """鼠标悬停"""
        el = self.driver.find_element(*locator)
        action = ActionChains(self.driver)
        action.move_to_element(el).perform()
        return self

# ------------------------ END: 鼠标事件：双击，悬停，拖动 ------------------------ #
