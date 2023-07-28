@projects
Feature: 开源项目模块
    需求描述: 用户可以创建项目，导入项目，以及删除项目

    Background: 清除浏览器缓存，避免缓存影响用例
    Given 清除浏览器缓存

    Scenario: 登录状态下，通过右上角导航栏点击新建>新建项目按钮， 新建个人公有项目
        Given 打开浏览器，写入登录cookies
        And 刷新页面，保持登录态
        When 点击导航栏右上角的新建图标
        Then 点击新建图标下的新建项目按钮，进入新建项目页面
        When 输入项目名称：<name>， 项目标识：<identifier>, 项目简介：<desc>
        And 选择.gitignore: <gitignore>，开源许可证: <licence>，项目类别: <type>，项目语言: <language>
        And 点击：创建项目 按钮，提交新建项目表单
        Then 当前页面的url地址应该是：<host>/<project_url>
        And 当前应该不存在 私有 标签

    @todo
    Scenario: 登录状态下，通过右上角导航栏点击新建>新建项目按钮， 新建个人私有项目


    @todo
    Scenario: 登录状态下，通过右上角导航栏点击新建>导入项目按钮， 导入github项目（公开仓库）作为个人公开仓库



    @todo
    Scenario: 登录状态下，通过右上角导航栏点击新建>导入项目按钮， 导入gitee项目（公开仓库）作为个人公开仓库



    @todo
    Scenario: 登录状态下，通过右上角导航栏点击新建>导入项目按钮， 导入github项目（私有仓库）作为个人私有仓库


    @todo
    Scenario: 登录状态下，通过右上角导航栏点击新建>导入项目按钮， 导入gitee项目（私有仓库）作为个人私有仓库

