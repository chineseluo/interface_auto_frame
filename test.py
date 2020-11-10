#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : interface_auto_frame
@Time    : 2020/10/23 18:16
@Auth    : chineseluo
@Email   : 848257135@qq.com
@File    : test.py
@IDE     : PyCharm
------------------------------------
"""
from typing import Optional, Union, Text, Tuple
from pydantic import BaseModel, Field


class OSTTest(BaseModel):
    name: str = Field(alias="test")
    age: Union[Text, Tuple[Text, Text], None]


if __name__ == "__main__":
    a = OSTTest(test="33")
    print(a.age)
