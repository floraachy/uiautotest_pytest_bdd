# -*- coding: utf-8 -*-
# @Time    : 2021/8/10 10:15
# @Author  : Flora.Chen
# @File    : login_page.py
# @Software: PyCharm
# @Desc: 登录页面的元素定位 和 操作

# 标准库导入
import time
# 第三方库导入
from selenium.webdriver.common.by import By
# 本地应用/模块导入
from case_utils.basepage import BasePage
from case_utils.allure_handle import allure_step
from case_utils.url_handle import url_handle

# ------------------------------ 登录弹窗元素定位 ---------------------------------------#
# 弹框中的用户名输入框
username_on_pop = (By.XPATH, "//input[@name='username']")
# 弹框中的密码输入框
password_on_pop = (By.XPATH, "//input[@name='password']")
# 提交登录表单按钮
login_submit_button_on_pop = (By.XPATH, "//div[text()='登录']")
# 弹框的错误提示信息
error_pop = (By.XPATH, "//div[@class='ant-notification-notice-description']")

# ------------------------------ 登录页面元素定位 ---------------------------------------#
# 用户名输入框
username_on_page = (By.ID, "login_username")
# 密码输入框
password_on_page = (By.ID, "login_password")
# 提交登录表单按钮
login_submit_button_on_page = (By.XPATH, "//span[text()='登 录']/..")
# 登录错误的提示语
login_error_text = (By.XPATH, "//p[contains(@class, 'message')]")
# 下次自动登录
auto_login = (By.XPATH, "//span[contains(text(), '下次自动登录')]")
# 忘记密码
forget_password_button = (By.XPATH, "//span[contains(text(), '下次自动登录')]/../")
# 去注册
go_register_button = (By.XPATH, "//a[contains(text(), '注册')]")


# ------------------------------ 登录 操作 ---------------------------------------#
class LoginPage(BasePage):
    """
    弹窗登录 / 网页登录
    """

    def load(self, host):
        """访问首页"""
        full_url = url_handle(host, "/login")
        self.visit(full_url)
        allure_step(step_title=f"访问：{full_url}")
        return full_url

    def input_login_info_on_pop(self, login, password):
        """
        弹窗登录操作: 输入登录信息，包括用户名以及密码
        """
        self.wait_element_visibility(username_on_pop).send_keys(login)
        self.wait_element_visibility(password_on_pop).send_keys(password)
        time.sleep(5)
        allure_step(step_title=f"登录弹窗输入--> 用户名: {login}  密码：{password}")

    def input_login_info_on_page(self, login, password):
        """
        登录页面操作: 输入登录信息，包括用户名以及密码
        """
        self.wait_element_visibility(username_on_page).send_keys(login)
        self.wait_element_visibility(password_on_page).send_keys(password)
        time.sleep(5)
        allure_step(step_title=f"登录页面输入--> 用户名: {login}  密码：{password}")

    def submit_login_on_pop(self):
        """
        弹窗登录操作: 点击登录按钮，提交登录表单
        """
        self.wait_element_visibility(login_submit_button_on_pop).click()
        time.sleep(5)
        allure_step(step_title=f"登录弹窗中，点击登录按钮，提交登录表单")

    def submit_login_on_page(self):
        """
        登录页面操作: 点击登录按钮，提交登录表单
        """
        self.wait_element_visibility(login_submit_button_on_page).click()
        time.sleep(5)
        allure_step(step_title=f"登录页面中，点击登录按钮，提交登录表单")

    def get_error_pop_text(self):
        """弹框的错误提示"""
        elems = self.driver.find_elements(*error_pop)
        return [elem.text for elem in elems]

    def get_login_error_text(self):
        """
        登录失败的错误提示语句
        """
        elems = self.driver.find_elements(*login_error_text)
        return [elem.text for elem in elems][0]

    def login_button_class(self):
        """获取弹框中登录按钮的class属性"""
        return self.get_class(login_submit_button_on_pop)

    def check_auto_login_button(self):
        # 勾选自动登录
        self.click(auto_login)
        allure_step(step_title="勾选自动登录按钮")

    def click_go_register(self):
        """点击 去注册"""
        self.click(go_register_button)
        allure_step(step_title=f"点击去注册按钮，进入注册页面")

    def click_forget_password(self):
        """点击 忘记密码"""
        self.click(forget_password_button)
        allure_step(step_title=f"点击忘记密码按钮，进入找回密码页面")
