# -*- coding: utf-8 -*-
# @Time    : 2023/7/23 15:56
# @Author  : chenyinhua
# @File    : test_login.py
# @Software: PyCharm
# @Desc:

# 标准库导入
# 第三方库导入
from pytest_bdd import scenarios, given, when, then, parsers
from sttable import parse_str_table
# 本地应用/模块导入
from page.login_page import *
from page.common_page import *
from page.home_page import *
from page.projects.projects_page import *

scenarios('./login.feature')


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


@when(parsers.parse("弹窗中，我输入以下信息进行登录：\n{user_info}"))
def input_login_info_on_pop(driver, user_info):
    # 通过sttable.parse_str_table获取测试步骤中表格的内容
    # 获取到的格式是这样的：[{'用户名': 'xxxxxx', '密码': 'xxxxxx'}]
    users = parse_str_table(user_info)
    for row in users.rows:
        login = row["用户名"]
        password = row["密码"]
        LoginPage(driver).input_login_info_on_pop(login=login, password=password)


@when(parsers.parse("登录页面中，我输入以下信息进行登录：\n{user_info}"))
def input_login_info(driver, user_info):
    users = parse_str_table(user_info)
    for row in users.rows:
        login = row["用户名"]
        password = row["密码"]
        LoginPage(driver).input_login_info_on_page(login=login, password=password)


@when("弹窗中，点击: 登录按钮， 提交登录表单")
def submit_login_button_on_pop(driver):
    LoginPage(driver).submit_login_on_pop()


@when("登录页面中，点击: 登录按钮， 提交登录表单")
def submit_login_button_on_page(driver):
    LoginPage(driver).submit_login_on_page()


@then("当前页面的url地址应该是：<host>/explore")
def check_current_url_on_pop(driver, host):
    expected = f'{host}/explore'
    actual = CommonPage(driver).get_current_url()
    assert expected == actual


@then(parsers.parse("登录成功，当前页面的url地址应该是：<host>/{login}"))
def check_current_url_on_page(driver, host, login):
    expected = f'{host}/{login}'
    actual = CommonPage(driver).get_current_url()
    assert expected == actual


@then(parsers.parse("登录成功，右上角显示的用户昵称应该是：{login}"))
def check_username(driver, login):
    expected = CommonPage(driver).get_user_login()
    actual = login
    assert expected == actual


@then(parsers.parse("登录失败，页面有密码错误提示：{expected_error}"))
def check_login_error(driver, expected_error):
    expected = expected_error
    actual = LoginPage(driver).get_login_error_text()
    assert expected == actual


