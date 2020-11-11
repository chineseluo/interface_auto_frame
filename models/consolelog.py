#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : interface_auto_frame
@Time    : 2020/10/23 18:06
@Auth    : chineseluo
@Email   : 848257135@qq.com
@File    : consolelog.py
@IDE     : PyCharm
------------------------------------
"""
import json
import logging
from loguru import logger


def log_output(ost_model, ost_type):
    msg = f"\n================== {ost_type} details ==================\n"
    for key, value in ost_model.dict().items():
        if isinstance(value, dict):
            value = json.dumps(value, indent=4)

        msg += "{:<8} : {}\n".format(key, value)
    logger.debug(msg)


class OSTConsoleLog(object):
    pass
