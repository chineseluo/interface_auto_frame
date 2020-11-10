#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : interface_auto_frame
@Time    : 2020/10/12 16:46
@Auth    : chineseluo
@Email   : 848257135@qq.com
@File    : test_login.py
@IDE     : PyCharm
------------------------------------
"""
import pytest
import allure
from Base.requestEngine import start_run_case
from Common.StringOption.StringOperate import String
from Parameter.yamlChoice import Login


@allure.feature("Login")
class TestLogin:

    @allure.severity("blocker")
    @allure.story("Test Login")
    @allure.title("测试登录")
    def test_login(self):
        result = start_run_case(Login, "用户权限")
        print(result)
