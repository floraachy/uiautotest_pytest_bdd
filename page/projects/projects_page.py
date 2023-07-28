# -*- coding: utf-8 -*-
# @Time    : 2021/12/19 15:36
# @Author  : Administrator
# @File    : project_home_page.py
# @Software: PyCharm
# @Desc: 项目首页

# 第三方库导入
from selenium.webdriver.common.by import By
# 本地应用/模块导入
from case_utils.basepage import BasePage
from case_utils.allure_handle import allure_step
from case_utils.url_handle import url_handle


# ------------------------------ 元素定位 ---------------------------------------#


# ------------------------------ 操作 ---------------------------------------#
class ProjectsPage(BasePage):
    """项目首页"""

    def load(self, host):
        full_url = url_handle(host, "/explore")
        self.visit(full_url)
        allure_step(step_title=f"访问：{full_url}")
        return full_url
