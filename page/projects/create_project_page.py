# -*- coding: utf-8 -*-
# @Time    : 2023/7/14 14:52
# @Author  : chenyinhua
# @File    : create_project_page.py
# @Software: PyCharm
# @Desc:

# 标准库导入
import time
# 第三方库导入
from selenium.webdriver.common.by import By
# 本地应用/模块导入
from case_utils.basepage import BasePage
from case_utils.allure_handle import allure_step
from case_utils.url_handle import url_handle

# ------------------------------ 元素定位 ---------------------------------------#
# 导入仓库URL
export_url = (By.XPATH, "//input[@id='NewWorkForm_clone_addr']")
# 需要授权验证
authorization_button = (By.XPATH, "//p[contains(text(), '需要授权验证')]")
# 导入仓库的token
token_inputbox = (By.ID, "NewWorkForm_auth_token")
# 导入仓库来源的用户名
mirror_username = (By.XPATH, "//input[@id='NewWorkForm_auth_username']")
# 导入仓库来源的密码
mirror_password = (By.XPATH, "//input[@id='NewWorkForm_password']")

# 拥有者输入框
owner_inpubox = (By.XPATH, "//label[@title='拥有者']/../following-sibling::div//input")
# 项目名称
project_name = (By.XPATH, "//input[@id='NewWorkForm_name']")
# 项目标识
depository_name = (By.XPATH, "//input[@id='NewWorkForm_repository_name']")
# 项目简介
project_desc = (By.XPATH, "//textarea[@id='NewWorkForm_description']")

# .gitignore checkbox
gitignore_checkbox = (By.XPATH, "//input[@id='NewWorkForm_ignoreFlag']")
# .gitignore 输入框
gitignore_selectbox = (By.XPATH, "//div[@id='NewWorkForm_ignore']")
# .gitignore-下拉框值
gitignore_value = (By.XPATH, "//li[text()='{}']")

# 开源许可证 checkbox
certificate_checkbox = (By.XPATH, "//input[@id='NewWorkForm_licenseFlag']")
# 开源许可证 输入框
certificate_selectbox = (By.XPATH, "//div[contains(text(), '请选择开源许可证')]")
# 开源许可证-下拉框值
certificate_value = (By.XPATH, "//li[text()='{}']")

# 将项目设置为私有-默认是公有
is_private_checkbox = (By.XPATH, "//input[@id='NewWorkForm_private']")

# 项目类别 checkbox
project_type_checkbox = (By.XPATH, "//input[@id='NewWorkForm_categoreFlag']")
# 项目类别 输入框
project_type_selectbox = (By.XPATH, "//div[text()='请选择项目类别']")
# 项目类别-下拉框值
project_type_value = (By.XPATH, "//li[text()='{}']")

# 项目语言 checkbox
project_language_checkbox = (By.XPATH, "//input[@id='NewWorkForm_languageFlag']")
# 项目类别 输入框
project_language_selectbox = (By.XPATH, "//div[text()='请选择项目语言']")
# 项目语言-下拉框值
project_language_value = (By.XPATH, "//li[text()='{}']")

# 该仓库将是一个镜像(设置为镜像后，该项目为只读，不能进行push等相关操作)
mirror_type = (By.XPATH, "//input[@id='NewWorkForm_is_mirror']")

# 创建项目 按钮
create_project_button = (By.XPATH, "//span[text()='创建项目']/parent::button")
# 导入项目按钮
export_project_button = (By.XPATH, "//span[text()='导入项目']/parent::button")

# 导入项目时文案：正在从......迁移
syncing_text = (By.XPATH, "//div[contains(text(), '迁移')]")


# ------------------------------ 新建项目页面的 操作 ---------------------------------------#
class CreateProjectPage(BasePage):
    """
    新建项目页面
    """

    def load(self, host):
        """访问新建项目页面"""
        full_url = url_handle(host, "/test_projects/deposit/new")
        self.visit(full_url)
        allure_step(step_title=f"访问：{full_url}")
        return full_url

    def check_private_checkbox(self):
        """点击私有的checkbox"""
        self.click(is_private_checkbox)

    def input_project_name_identify_desc(self, name, identifier, desc):
        """
        输入项目名称，项目标识以及项目简介
        """
        # 输入项目名称
        self.input(project_name, name)
        allure_step(step_title=f"输入项目名称：{name}")
        # 输入项目标识
        self.input(depository_name, identifier)
        allure_step(step_title=f"输入项目标识：{identifier}")
        # 输入项目简介
        self.input(project_desc, desc)
        allure_step(step_title=f"输入项目名称：{desc}")

    def choose_project_type_language(self, language, category):
        """
        选择项目类别和语言
        步骤：
        1. 勾选checkbox
        2. 点击输入框
        3. 选择项目类别/语言
        """
        time.sleep(2)
        # 选择项目类别
        self.click(project_type_checkbox)
        self.click(project_type_selectbox)
        pattern, locator = project_type_value
        self.click((pattern, locator.format(category)))
        allure_step(step_title=f"选择项目类别：{category}")

        # 往下滑动
        js = "window.scrollTo(0, 200)"
        self.execute_js(js)

        time.sleep(2)
        # 选择项目语言
        self.click(project_language_checkbox)
        self.click(project_language_selectbox)
        pattern, locator = project_language_value
        self.click((pattern, locator.format(language)))
        allure_step(step_title=f"选择项目语言：{language}")
        time.sleep(2)

    def choose_project_gitignore_licence(self, gitignore, license):
        """
           选择gitignore以及开源许可证
           步骤：
           1. 勾选checkbox
           2. 点击输入框
           3. 选择项目类别/语言
           """
        # 选择gitignore
        self.click(gitignore_checkbox)
        self.click(gitignore_selectbox)
        pattern, locator = gitignore_value
        self.click((pattern, locator.format(gitignore)))
        allure_step(step_title=f"选择gitignore：{gitignore}")

        # 选择开源许可证
        self.click(certificate_checkbox)
        self.click(certificate_selectbox)
        pattern, locator = certificate_value
        self.click((pattern, locator.format(license)))
        allure_step(step_title=f"选择开源许可证：{license}")
        time.sleep(1)

    def submit_new_project(self):
        # 点击创建项目按钮
        self.click(create_project_button)
        allure_step(step_title="点击创建项目按钮，提交新建项目表单")
        time.sleep(5)

    def new_project(self, **kwargs):
        """
        新建项目
        """
        # 输入项目名称，项目标识以及项目简介
        self.input_project_name_identify_desc(name=kwargs.get('name'), identifier=kwargs.get('identifier'),
                                              desc=kwargs.get('desc'))
        # 选择gitignore以及开源许可证
        self.choose_project_gitignore_licence(**kwargs)

        if kwargs.get("private"):
            # 设置项目为私有
            self.check_private_checkbox()
            allure_step(step_title=f"勾选项目为私有仓库")

        # 选择项目类别和语言
        self.choose_project_type_language(**kwargs)

        # 点击创建项目按钮
        self.submit_new_project()

    def export_project(self, **kwargs):
        """
        导入项目
        """
        # 输入镜像地址
        self.input(export_url, kwargs.get("mirror_url"))
        allure_step(step_title=f"输入导入仓库地址：{kwargs.get('mirror_url')}")

        if kwargs.get("mirror_private"):
            self.click(authorization_button)
            allure_step(step_title=f"点击输入授权验证")
            if kwargs.get("mirror_url").startswith("https://github.com"):
                self.input(token_inputbox, kwargs.get("auth_token"))
                allure_step(step_title=f"输入平台用户授权token：{kwargs.get('auth_token')}")
            else:
                self.input(mirror_username, kwargs.get("auth_user"))
                self.input(mirror_password, kwargs.get("auth_password"))
                allure_step(step_title=f"输入导入仓库对应用户名及密码：{kwargs.get('mirror_user')}， {kwargs.get('mirror_pwd')}")

        # 输入项目名称，项目标识以及项目简介
        self.input_project_name_identify_desc(name=kwargs.get('name'), identifier=kwargs.get('identifier'),
                                              desc=kwargs.get('desc'))
        if kwargs.get("private"):
            # 设置项目为私有
            self.check_private_checkbox()
            allure_step(step_title=f"勾选项目为私有仓库")

        if kwargs.get("mirror_type"):
            # 该仓库将是一个镜像(设置为镜像后，该项目为只读，不能进行push等相关操作)
            self.click(mirror_type)
            allure_step(step_title=f"勾选该仓库是一个镜像仓库")

        # 选择项目类别和语言
        self.choose_project_type_language(**kwargs)

        # 点击导入项目按钮
        self.click(export_project_button)
        allure_step(step_title="点击导入项目按钮，提交导入项目表单")
        time.sleep(5)
