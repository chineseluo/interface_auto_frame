#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : interface_auto_frame
@Time    : 2020/8/25 16:07
@Auth    : chineseluo
@Email   : 848257135@qq.com
@File    : conftest.py
@IDE     : PyCharm
------------------------------------
"""
import allure
import pytest


@pytest.fixture()
def function_fixture():
    print("运行于函数前")
    yield
    print("运行于函数后")
