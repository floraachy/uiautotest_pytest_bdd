# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/9 16:41
# @Author  : chenyinhua
# @File    : url_handle.py
# @Software: PyCharm
# @Desc: 根据配置文件中的域名，以及测试用例数据中的url处理访问url

# 第三方库导入
from loguru import logger


def url_handle(host, url):
    """
    将host以及url拼接组成full_url
    """
    try:
        """
        用例数据中获取到的url(一般是不带host的，个别特殊的带有host，则不进行处理)
        """
        # 从用例数据中获取url，如果键url不存在，则返回空字符串
        # 如果url是以http开头的，则直接使用该url，不与host进行拼接
        if url.lower().startswith("http"):
            full_url = url
        else:
            # 如果host以/结尾 并且 url以/开头
            if host.endswith("/") and url.startswith("/"):
                full_url = host[0:len(host) - 1] + url
            # 如果host以/结尾 并且 url不以/开头
            elif host.endswith("/") and (not url.startswith("/")):
                full_url = host + url
            elif (not host.endswith("/")) and url.startswith("/"):
                # 如果host不以/结尾 且 url以/开头，则将host和url拼接起来，组成新的url
                full_url = host + url
            else:
                # 如果host不以/结尾 且 url不以/开头，则将host和url拼接起来的时候增加/，组成新的url
                full_url = host + "/" + url
        return full_url
    except Exception as e:
        logger.error(f"处理url报错了：{e}")
        print(f"处理url报错了：{e}")
