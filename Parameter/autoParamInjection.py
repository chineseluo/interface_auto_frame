#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : interface_auto_frame
@Time    : 2020/8/25 16:17
@Auth    : chineseluo
@Email   : 848257135@qq.com
@File    : autoParamInjection.py
@IDE     : PyCharm
------------------------------------
"""
import yaml
import os
import logging
from Common.FileOption.comFileOption import get_roots_dirs_files_list
from Common.FileOption.yamlOption import YamlFileOption


class AutoInjection:
    def __init__(self, *args):
        self.interface_info = []
        self.__read_yaml(*args)

    def __read_yaml(self, *args):
        if len(args) == 1:
            yaml_path = os.path.join(os.path.dirname(__file__), args[0], args[0] + ".yml")
            self.interface_info = YamlFileOption().read_yaml(yaml_path)['parameters']
        elif len(args) == 2:
            yaml_path = os.path.join(os.path.dirname(__file__), args[0], args[1] + ".yml")
            self.interface_info = YamlFileOption().read_yaml(yaml_path)['parameters']
        else:
            logging.error("参数传递错误，只能接收两个参数")

    def get_param_by_url(self, url):
        param_dict = {}
        for item in self.interface_info:
            if item["url"] == url:
                param_dict = item
        return param_dict


class Login(AutoInjection):
    def __init__(self):
        super(Login, self).__init__(self.__class__.__name__)


if __name__ == '__main__':
    t = Login()
    print(t.get_param_by_url("/api/invpn/users"))
