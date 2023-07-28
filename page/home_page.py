# -*- coding: utf-8 -*-
# @Time    : 2023/7/11 17:24
# @Author  : chenyinhua
# @File    : home_page.py
# @Software: PyCharm
# @Desc:


# 第三方库导入
from selenium.webdriver.common.by import By
# 本地应用/模块导入
from case_utils.basepage import BasePage
from case_utils.allure_handle import allure_step


# ------------------------------ 元素定位 ---------------------------------------#


# ------------------------------ 首页各项 操作 ---------------------------------------#
class HomePage(BasePage):
    """
    GitLink首页
    """

    def load(self, host):
        """访问首页"""
        full_url = host
        self.visit(full_url)
        allure_step(step_title=f"访问：{full_url}")
        return full_url
