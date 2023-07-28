# -*- coding: utf-8 -*-
# @Time    : 2023/7/14 14:47
# @Author  : chenyinhua
# @File    : common_page.py
# @Software: PyCharm
# @Desc:

# 标准库导入
import time
# 第三方库导入
from selenium.webdriver.common.by import By
# 本地应用/模块导入
from case_utils.basepage import BasePage
from case_utils.allure_handle import allure_step

# ------------------------------ 元素定位 ---------------------------------------#
# 游客状态下的 登录按钮
login_button = (By.XPATH, "//a[text()='登录']")
# 用户登录状态下，右上角新建项目/导入项目/新建组织/加入项目的图标
new_project_icon = (By.XPATH, "//i[contains(@class, 'icon-sousuo')]/following-sibling::img")
# 用户登录状态下，新建项目
create_project = (By.XPATH, "//a[text()='新建项目']")
# 用户登录状态下，导入项目
export_project = (By.XPATH, "//a[text()='导入项目']")
# 用户登录状态下，新建组织
create_organization = (By.XPATH, "//a[text()='新建组织']")
# 用户登录状态下，加入项目
join_project = (By.XPATH, "//a[text()='加入项目']")

# 右上角的用户登录后的头像
avatar = (By.XPATH, "//a[@class='ant-dropdown-trigger']")


# ------------------------------ 公共模块的一些 操作 ---------------------------------------#
class CommonPage(BasePage):
    """
    公共模块的一些操作，如 导航栏，底部，公共弹窗
    """

    def get_current_url(self):
        """
        获取当前浏览器驱动的地址
        """
        url = super().get_current_url()
        allure_step(step_title=f"当前浏览器驱动地址：{url}")
        return url

    def click_login_button(self):
        """
        游客状态下 点击 右上角 “登录”按钮
        """
        self.wait_element_clickable(login_button).click()
        allure_step(step_title="游客状态下 点击 右上角 登录 按钮")

    def click_new_icon(self):
        """
        登录状态下，点击 新建 图标
        显示按钮：新建项目，导入项目，新建组织，加入项目
        """
        self.hover(new_project_icon)
        time.sleep(2)
        allure_step(step_title=f"登录状态下，点击右上角 新建 图标，显示：新建项目，导入项目，新建组织，加入项目")

    def click_create_project_button(self):
        """
        登录状态下，点击右上角 新建>新建项目 按钮
        """
        self.click(create_project)
        allure_step(step_title=f"登录状态下，点击右上角 新建>新建项目 按钮")

    def click_export_project_button(self):
        """
        登录状态下，点击右上角 新建>导入项目 按钮
        """
        self.click(export_project)
        allure_step(step_title=f"登录状态下，点击右上角 新建>导入项目 按钮")

    def click_create_org_button(self):
        """
        登录状态下，点击右上角 新建>新建组织 按钮
        """
        self.click(create_organization)
        allure_step(step_title=f"登录状态下，点击右上角 新建>导入项目 按钮")

    def click_join_project_button(self):
        """
        登录状态下，点击右上角 新建>加入项目 按钮
        """
        self.click(join_project)
        allure_step(step_title=f"登录状态下，点击右上角 新建>加入项目 按钮")

    def get_user_login(self):
        """获取用户头像"""
        login = self.get_element_attribute(avatar, "href").split("/")[-1]
        allure_step(step_title=f"获取到的用户login是：{login}")
        return login
