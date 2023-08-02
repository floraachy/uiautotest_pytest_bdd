# -*- coding: utf-8 -*-
# @Time    : 2023/3/17 18:33
# @Author  : Flora.Chen
# @File    : conftest.py
# @Software: PyCharm
# @Desc:

# 标准库导入
# 第三方库导入
import pytest
import requests
from loguru import logger
from pytest_bdd import given, then
# 本地应用/模块导入
from config.settings import RunConfig
from config.global_vars import GLOBAL_VARS
from case_utils.get_driver import GetDriver
from case_utils.allure_handle import allure_step
from common_utils.base_request import BaseRequest


@pytest.fixture(scope="session")
def driver():
    # logger.debug(f"此时的driver类型:{RunConfig.driver_type}")
    driver = GetDriver(driver_type=RunConfig.driver_type).get_driver()
    RunConfig.driver = driver
    yield driver
    driver.close()
    driver.quit()


@pytest.fixture(scope="session")
def host():
    return GLOBAL_VARS.get("host")


@given("清除浏览器缓存")
def clear_cache(driver):
    driver.delete_all_cookies()
    allure_step(step_title="清除浏览器缓存")


@given(name="打开浏览器，写入登录cookies")
def write_login_cookies(driver, login_api):
    # 遍历 cookies 字典并添加到 WebDriver 中
    login_cookies = login_api[0]
    for name, value in login_cookies.items():
        """
        add_cookie() 方法是 WebDriver 的方法，用于向浏览器添加 cookie。正确的方法调用应该只有两个参数：name 和 value
        """
        driver.add_cookie({"name": name, "value": value})


@given(name="刷新页面，保持登录态")
def refresh_page(driver):
    driver.refresh()


@pytest.fixture(scope="module")
def login_api():
    """
    获取登录的cookie
    :return:
    """
    host = GLOBAL_VARS.get("host")
    login = GLOBAL_VARS.get('login')
    password = GLOBAL_VARS.get('password')
    # 兼容一下host后面多一个斜线的情况
    if host[-1] == "/":
        host = host[:len(host) - 1]
    req_data = {
        "url": host + "/api/accounts/login.json",
        "method": "POST",
        "request_type": "json",
        "headers": {"Content-Type": "application/json; charset=utf-8;"},
        "payload": {"login": login, "password": password, "autologin": 1}
    }
    # 请求登录接口
    try:
        res = BaseRequest.send_request(req_data=req_data)
        res.raise_for_status()
        # 将cookies转成字典
        cookies = requests.utils.dict_from_cookiejar(res.cookies)
        logger.debug(f"获取用户：{login}登录的cookies成功：{type(cookies)} || {cookies}")
        yield cookies, res.json()
    except Exception as e:
        GLOBAL_VARS["login_cookie"] = None
        logger.error(f"获取用户：{login}登录的cookies失败：{e}")
