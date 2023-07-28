# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/2/2 16:05
# @Author  : chenyinhua
# @File    : conftest.py
# @Software: PyCharm
# @Desc: 这是文件的描述信息

# 标准库导入
import re
import time
import os
from time import strftime
from datetime import datetime
# 第三方库导入
from loguru import logger
from py._xmlgen import html  # 安装pytest-html，版本最好是2.1.1
import pytest
# 本地应用/模块导入
from config.global_vars import ENV_VARS, GLOBAL_VARS
from config.path_config import IMG_DIR
from config.settings import RunConfig
from case_utils.allure_handle import allure_step
from case_utils.basepage import BasePage


# ------------------------------------- START: pytest-bdd钩子函数处理---------------------------------------#
def pytest_bdd_apply_tag(tag, function):
    """
    自定义标记转换为 pytest 标记的行为
    """
    print(f"标记是什么：{tag}")
    if tag == 'todo':
        marker = pytest.mark.skip(reason="还没有处理完成~")
        marker(function)
        return True
    else:
        # todo 怎么样可以注册pytest自定义的标记呢  我这样写好像没有报错，不确定是否可以
        setattr(pytest.mark, tag, f"pytest.mark.{tag}")
        return True


def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    """
    当步骤函数执行失败时，pytest_bdd_step_error 钩子会被触发
    :param request: 包含有关测试请求的信息。
    :param feature: 当前特性的元数据。
    :param scenario: 当前场景的元数据。
    :param step: 当前步骤的元数据。
    :param step_func: 当前步骤的函数对象。
    :param step_func_args: 当前步骤的函数参数。
    :param exception: 捕获到的异常对象。
    :return:
    """

    feature_name = getattr(feature, 'name', None)
    feature_description = getattr(feature, 'description', None)

    scenario_name = getattr(scenario, 'name', None)

    logger.error("\n" + "=" * 80
                 + "\n-------------测试步骤出错了--------------------\n"
                   f"Feature: {feature_name}\n"
                   f"Scenario: {scenario_name}\n"
                   f"Step: {step}\n"
                   f"Exception:   {exception}\n"
                 + "=" * 80)
    print("\n" + "=" * 80
                 + "\n-------------测试步骤出错了--------------------\n"
                   f"Feature: {feature_name}\n"
                   f"Scenario: {scenario_name}\n"
                   f"Step: {step}\n"
                   f"Exception:   {exception}\n"
                 + "=" * 80)

    # 堆栈跟踪
    # logger.error(f"Stack trace: {exception.__traceback__}\n")


# ------------------------------------- END: pytest-bdd钩子函数处理---------------------------------------#

# ------------------------------------- START: pytest钩子函数处理---------------------------------------#
def pytest_configure(config):
    """
    1. 在测试运行前，修改Environment部分信息，配置测试报告环境信息
    2. 注册自定义标记
    """
    # 给环境表 添加项目名称及开始时间
    config._metadata["项目名称"] = ENV_VARS["common"]["project_name"]
    config._metadata['开始时间'] = strftime('%Y-%m-%d %H:%M:%S')
    # 给环境表 移除packages 及plugins
    config._metadata.pop("Packages")
    config._metadata.pop("Plugins")


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    """
    在测试运行后，修改Environment部分信息
    """
    # 给环境表 添加 项目环境
    session.config._metadata['项目环境'] = GLOBAL_VARS.get("host", "")


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    """设置列"用例描述"的值为用例的标题title"""
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    # 获取调用结果的测试报告，返回一个report对象
    # report对象的属性包括when（steup, call, teardown三个值）、nodeid(测试用例的名字)、outcome(用例的执行结果，passed,failed)
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == "call" or report.when == "setup":
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            # 截图
            driver = RunConfig.driver
            if driver:
                logger.debug(f"{driver}： 开始进行截图操作......")
                # 创建不同浏览器驱动保存截图的目录
                driver_dir = os.path.join(IMG_DIR, RunConfig.driver_type)
                os.makedirs(driver_dir, exist_ok=True)
                file_name = str(report).split(" ")[1].split("::")[1].replace("'", "") + "_" + datetime.now().strftime(
                    "%Y-%m-%d %H_%M_%S") + ".png"
                BasePage(driver=driver).screenshot(path=driver_dir, filename=file_name)
                img_path = os.path.join(driver_dir, file_name)
                if img_path:
                    #  报错截图添加到allure-pytest报告
                    allure_step(step_title="点击查看失败截图......", content=report.nodeid, source=img_path)
                    # 报错截图添加到pytest-html报告
                    html = f'<div class="image"><img src="{img_path}" onclick="window.open(this.src)"/></div>'
                    extra.append(pytest_html.extras.html(html))


def pytest_terminal_summary(terminalreporter, config):
    """
    收集测试结果
    """
    _RERUN = len([i for i in terminalreporter.stats.get('rerun', []) if i.when != 'teardown'])
    try:
        # 获取pytest传参--reruns的值
        reruns_value = int(config.getoption("--reruns"))
        _RERUN = int(_RERUN / reruns_value)
    except Exception:
        reruns_value = "未配置--reruns参数"
        _RERUN = len([i for i in terminalreporter.stats.get('rerun', []) if i.when != 'teardown'])

    _PASSED = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    _ERROR = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    _FAILED = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    _SKIPPED = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    _XPASSED = len([i for i in terminalreporter.stats.get('xpassed', []) if i.when != 'teardown'])
    _XFAILED = len([i for i in terminalreporter.stats.get('xfailed', []) if i.when != 'teardown'])

    _TOTAL = terminalreporter._numcollected
    _TIMES = time.time() - terminalreporter._sessionstarttime
    logger.success(f"\n======================================================\n"
                   "-------------测试结果--------------------\n"
                   f"用例总数: {_TOTAL}\n"
                   f"跳过用例数: {_SKIPPED}\n"
                   f"实际执行用例总数: {_PASSED + _FAILED + _XPASSED + _XFAILED}\n"
                   f"通过用例数: {_PASSED}\n"
                   f"异常用例数: {_ERROR}\n"
                   f"失败用例数: {_FAILED}\n"
                   f"重跑的用例数(--reruns的值): {_RERUN}({reruns_value})\n"
                   f"意外通过的用例数: {_XPASSED}\n"
                   f"预期失败的用例数: {_XFAILED}\n\n"
                   "用例执行时长: %.2f" % _TIMES + " s\n")
    try:
        _RATE = _PASSED / (_TOTAL - _SKIPPED) * 100
        logger.success(
            f"\n用例成功率: %.2f" % _RATE + " %\n"
                                       "=====================================================")
    except ZeroDivisionError:
        logger.critical(
            f"用例成功率: 0.00 %\n"
            "=====================================================")


# ------------------------------------- END: pytest钩子函数处理---------------------------------------#

# ------------------------------------- START: pytest-html钩子函数处理 ---------------------------------------#

def pytest_html_report_title(report):
    """
    修改报告标题
    """
    report.title = f'{ENV_VARS["common"]["project_name"]} {ENV_VARS["common"]["report_title"]}'


def pytest_html_results_summary(prefix, summary, postfix):
    """
    修改Summary部分的信息
    """
    prefix.extend([html.p(f'测试人员：{ENV_VARS["common"]["tester"]}')])
    prefix.extend([html.p(f'所属部门: ：{ENV_VARS["common"]["department"]}')])


def pytest_html_results_table_header(cells):
    """
    修改结果表的表头
    """
    cells.pop(1)  # 移除 "Test" 列
    # 往表格中增加一列"用例描述"，并且给"用例描述"增加排序
    cells.insert(0, html.th('用例描述', class_="sortable", col="name"))
    # 往表格中增加一列"用例方法"，并且给"用例方法"增加排序
    cells.insert(1, html.th('用例方法', class_="sortable", col="name"))
    # 往表格中增加一列"执行时间"，并且给"执行时间"增加排序
    cells.insert(2, html.th('执行时间', class_="sortable time", col="time"))


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    """
    修改结果表的表头后给对应的行增加值
    """
    cells.pop(1)  # 移除 "Test" 列
    # 往列"用例描述"插入每行的值
    cells.insert(0, html.td(report.description))
    # 往列"用例方法"插入每行的值
    cells.insert(1, html.td(report.func))
    # 往列"执行时间"插入每行的值
    cells.insert(2, html.td(strftime("%Y-%m-%d %H:%M:%S"), class_="col-time"))


def pytest_html_results_table_html(report, data):
    """如果测试通过，则显示这条用例通过啦！"""
    if report.passed:
        del data[:]
        data.append(html.div("这条用例通过啦！", class_="empty log"))

# ------------------------------------- END: pytest-html钩子函数处理 ---------------------------------------#
