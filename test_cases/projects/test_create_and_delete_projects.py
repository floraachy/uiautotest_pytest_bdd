# -*- coding: utf-8 -*-
# @Time    : 2023/7/24 11:26
# @Author  : chenyinhua
# @File    : test_create_and_delete_projects.py
# @Software: PyCharm
# @Desc:

# 标准库导入
import random
# 第三方库导入
from pytest_bdd import scenarios, given, when, then, parsers
from loguru import logger
# 本地应用/模块导入
from page.projects.create_project_page import CreateProjectPage
from page.common_page import CommonPage
from page.projects.project_detail_page import ProjectDetailPage
from case_utils.data_handle import data_handle, eval_data_process
from config.global_vars import GLOBAL_VARS

scenarios('../../test_features/projects/create_and_delete_projects.feature')

case = {
    "name": "Auto Test ${generate_name()}",
    "identifier": "${generate_identifier()}",
    "desc": "${generate_name()}",
    "category": random.choice(["机器学习", "大数据", "深度学习", "人工智能", "量子计算", "智慧医疗", "自动驾驶", "其他"]),
    "language": random.choice(["C#", "HTML", "CSS", "Python3.6"]),
    "gitignore": random.choice(["Ada", "Actionscript", "Ansible", "Android", "Agda"]),
    "license": random.choice(["0BSD", "AAL", "AFL-1.1", "389-exception"]),
}
case = eval_data_process(data_handle(obj=case, source=GLOBAL_VARS))

logger.debug(f"打印用例，定位一下：{case}")


@when(name="点击导航栏右上角的新建图标")
def click_new_icon(driver):
    CommonPage(driver).click_new_icon()


@then(name="点击新建图标下的新建项目按钮，进入新建项目页面")
def click_new_project_button(driver):
    CommonPage(driver).click_create_project_button()


@when(name="输入项目名称：<name>， 项目标识：<identifier>, 项目简介：<desc>")
def input_name_identifier_desc(driver, name=case["name"], identifier=case["identifier"], desc=case["desc"]):
    CreateProjectPage(driver).input_project_name_identify_desc(name, identifier, desc)


@when(name="选择.gitignore: <gitignore>，开源许可证: <licence>，项目类别: <type>，项目语言: <language>")
def choose_gitignore_licence_language_type(driver, gitignore=case["gitignore"], license=case["license"],
                                           language=case["language"], category=case["category"]):
    CreateProjectPage(driver).choose_project_gitignore_licence(gitignore=gitignore, license=license)
    CreateProjectPage(driver).choose_project_type_language(language=language, category=category)


@when(name="点击：创建项目 按钮，提交新建项目表单")
def submit_project_button(driver):
    CreateProjectPage(driver).submit_new_project()


@then("当前页面的url地址应该是：<host>/<project_url>")
def check_current_url(driver, host, project_url=f'{GLOBAL_VARS["login"]}/{case["identifier"]}'):
    expected = f"{host}/{project_url}"
    actual = CommonPage(driver).get_current_url()
    assert expected == actual


@then("当前应该不存在 私有 标签")
def check_private_tag(driver):
    expected = False
    actual = ProjectDetailPage(driver).get_project_private_tag()
    assert expected == actual
