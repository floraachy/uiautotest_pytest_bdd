@login
Feature: 登录模块
    需求描述: 用户进入登录页面/弹窗登录页面，使用正确用户名以及密码可以登录成功

    Background: 清除浏览器缓存，避免缓存影响用例
        Given 清除浏览器缓存

    Scenario: 弹窗登录: 正确用户名和密码登录成功
        Given 打开浏览器，访问项目首页<host>/explore
        When 点击:登录按钮，打开登录弹窗
        And 弹窗中，输入用户：<login>， 密码：<password>
        And 弹窗中，点击: 登录按钮， 提交登录表单
        Then 当前页面的url地址应该是：{host}/explore
        And 右上角显示的用户昵称应该是：<login>

    Scenario: 网页登录: 正确用户名和密码登录成功
        Given 打开浏览器，访问GitLink首页<host>
        When 点击:登录按钮，进入登录页面
        And 登录页面中，输入用户：<login>， 密码：<password>
        And 登录页面中，点击: 登录按钮， 提交登录表单
        Then 当前页面的url地址应该是：<host>/<login>
        And 右上角显示的用户昵称应该是：<login>
