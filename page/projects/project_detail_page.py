# -*- coding: utf-8 -*-
# @Time    : 2023/7/14 16:07
# @Author  : chenyinhua
# @File    : project_detail_page.py
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

# ------------------------------项目详情页 元素定位---------------------------------------#
# 私有仓库标识图标
project_status_tag = (By.XPATH, "//span[text()='私有']")
# 同步镜像按钮
sync_mirror_button = (By.XPATH, "//a[text()='同步镜像']")
# 仓库设置tab
repository_settings = (By.XPATH, "//span[text()='仓库设置']")
# 删除仓库按钮
delete_repository_button = (By.XPATH, "//span[text()='删除本仓库']")
# 确定按钮
confirm_button = (By.XPATH, "//a[text()='确定']")
# 仓库删除成功提示语
delete_repository_success = (By.XPATH, "//div[text()='仓库删除成功！']")

# 易修tab
issue_tab = (By.XPATH, "//span[text()='疑修(Issue)']")
# 创建易修按钮
new_issue_button = (By.XPATH, "//a[contains(text(), '创建疑修')]")
# 易修标题
issue_title_inputbox = (By.ID, "NewOrderForm_subject")
# 易修内容
issue_content_codemirror = "//textarea[@id='mdEditors_order-new-description']/following::div[contains(@class, 'CodeMirror-wrap')]"
# 上传文件按钮
upload_file_button = (By.XPATH, "//p[text()='拖动文件或点击此处上传']")
# 创建易修按钮
create_issue_button = (By.XPATH, "//span[text()='创 建']/parent::button")
# 任务创建成功提示
issue_create_success = (By.XPATH, "//div[text()='任务创建成功！']")


# ------------------------------项目详情页 操作---------------------------------------#
class ProjectDetailPage(BasePage):
    """
    项目详情页
    """

    def load(self, host, project_url):
        """访问项目详情页"""
        full_url = url_handle(host, project_url)
        self.visit(full_url)
        return full_url

    def get_project_private_tag(self):
        """获取项目的状态标签（私有项目会有私有tag）"""
        if self.find_elements(project_status_tag):
            allure_step(step_title="存在：私有tag")
            return True
        else:
            allure_step(step_title="不存在：私有tag")
            return False

    def get_sync_mirror_button(self):
        """同步镜像按钮是否存在"""
        if self.find_elements(sync_mirror_button):
            allure_step(step_title="存在：同步镜像按钮")
            return True
        else:
            allure_step(step_title="不存在：同步镜像按钮")
            return False

    def delete_project(self):
        """删除仓库"""
        time.sleep(2)
        allure_step(step_title="在项目详情页，点击'仓库设置'按钮")
        self.click(repository_settings)
        time.sleep(2)
        allure_step(step_title="往下滑动 440像素")
        js = "window.scrollTo(0, 440)"
        self.execute_js(js)
        allure_step(step_title="点击删除仓库按钮")
        self.click(delete_repository_button)
        allure_step(step_title="弹出框中点击确定按钮")
        self.click(confirm_button)

    def get_delete_project_success_text(self):
        """仓库删除成功提示语"""
        if self.find_elements(delete_repository_success):
            allure_step(step_title="有提示语：仓库删除成功！")
            return True
        else:
            allure_step(step_title="没有提示语：仓库删除成功！")
            return False

    def click_issue_tab(self):
        """点击issue tab"""
        self.click(issue_tab)
        return self

    def input_content_to_codemirror(self, content):
        """
        issue以及合并请求的编辑器使用的都是codeMirror,
        不能直接使用selenium对定位到的元素进行操作
        """
        elem = self.driver.find_element_by_xpath(issue_content_codemirror)
        self.execute_js("arguments[0].CodeMirror.setValue(arguments[1]);", elem, content)
        return self

    def create_issue(self, **kwargs):
        """创建易修"""
        # 点击易修tab
        self.click_issue_tab()
        # 刷新页面
        self.refresh()
        time.sleep(5)
        # 点击创建易修按钮
        self.click(new_issue_button)
        time.sleep(1)
        # 输入易修标题
        self.input(issue_title_inputbox, kwargs.get("issue_title"))
        time.sleep(1)
        # 输入易修内容
        self.input_content_to_codemirror(kwargs.get("issue_content"))
        # 上传易修附件
        self.click(upload_file_button)
        time.sleep(2)
        self.upload_file_pyautogui(kwargs.get("issue_attachments"))
        # 点击创建按钮
        self.click(create_issue_button)
        return self

    def issue_create_success(self):
        """易修创建成功的提示语"""
        if self.find_elements(issue_create_success):
            return True
        else:
            return False
