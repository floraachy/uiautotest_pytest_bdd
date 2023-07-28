# -*- coding: utf-8 -*-
# @Time    : 2023/7/23 15:56
# @Author  : chenyinhua
# @File    : test_login.py
# @Software: PyCharm
# @Desc:

# 标准库导入
# 第三方库导入
from pytest_bdd import scenario, given, when, then, parsers
# 本地应用/模块导入
from page.login_page import *
from page.common_page import *
from page.home_page import *
from page.projects.projects_page import *
from config.global_vars import GLOBAL_VARS

user = {
    "login": GLOBAL_VARS.get("login"),
    "password": GLOBAL_VARS.get("password")
}


@scenario('../test_features/login.feature', '弹窗登录: 正确用户名和密码登录成功')
def test_pop_login_success():
    pass


@scenario('../test_features/login.feature', '网页登录: 正确用户名和密码登录成功')
def test_page_login_success():
    pass


@given("打开浏览器，访问项目首页<host>/explore")
def visit_projects_home(driver, host):
    ProjectsPage(driver).load(host)


@given("打开浏览器，访问GitLink首页<host>")
def visit_home(driver, host):
    HomePage(driver).load(host)


@when("点击:登录按钮，进入登录页面")
@when("点击:登录按钮，打开登录弹窗")
def click_login_button(driver):
    CommonPage(driver).click_login_button()


@when(parsers.parse("弹窗中，输入用户：<login>， 密码：<password>"))
def input_login_info_on_pop(driver, login=user["login"], password=user["password"]):
    LoginPage(driver).input_login_info_on_pop(login=login, password=password)


@when(parsers.parse("登录页面中，输入用户：<login>， 密码：<password>"))
def input_login_info(driver, login=user["login"], password=user["password"]):
    LoginPage(driver).input_login_info_on_page(login=login, password=password)


@when("弹窗中，点击: 登录按钮， 提交登录表单")
def submit_login_button_on_pop(driver):
    LoginPage(driver).submit_login_on_pop()


@when("登录页面中，点击: 登录按钮， 提交登录表单")
def submit_login_button_on_page(driver):
    LoginPage(driver).submit_login_on_page()


@then("当前页面的url地址应该是：{host}/explore")
def check_current_url_on_pop(driver, host):
    expected = f'{host}/explore'
    actual = CommonPage(driver).get_current_url()
    assert expected == actual


@then("当前页面的url地址应该是：<host>/<login>")
def check_current_url_on_page(driver, host, login=user["login"]):
    expected = f'{host}/{login}'
    actual = CommonPage(driver).get_current_url()
    assert expected == actual


@then("右上角显示的用户昵称应该是：<login>")
def check_username(driver, login=user["login"]):
    expected = CommonPage(driver).get_user_login()
    actual = login
    assert expected == actual
