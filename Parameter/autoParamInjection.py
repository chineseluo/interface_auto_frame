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
    """自动yaml对象注入
    通过继承AutoInjection,对子类进行基础属性赋值
    """
    def __init__(self, *args):
        self.interface_info = []
        self.__read_yaml(*args)
        logging.info(f"{self.__class__.__name__} Yaml object injection in progress")

    def __read_yaml(self, *args):
        """
        接口yaml对象读取，通过子类继承父类AutoInjection，子类初始化时，向上转型，到对应子类yaml模块中读取yaml文件
        :param args:
        :return:
        """
        if len(args) == 1:
            yaml_path = os.path.join(os.path.dirname(__file__), args[0], args[0] + ".yml")
            self.interface_info = YamlFileOption().read_yaml(yaml_path)['parameters']
        elif len(args) == 2:
            yaml_path = os.path.join(os.path.dirname(__file__), args[0], args[1] + ".yml")
            self.interface_info = YamlFileOption().read_yaml(yaml_path)['parameters']
        else:
            logging.error("参数传递错误，只能接收两个参数")

    def get_param_by_yaml(self, params_mark) -> dict:
        param_dict = {}
        if isinstance(params_mark, str):
            for item in self.interface_info:
                if item["desc"] == params_mark:
                    param_dict = item
                    return param_dict
                else:
                    logging.error("从yaml文件中获取接口参数失败，请检查yaml文件对应关系，错误参数为：{}".format(params_mark))
        elif isinstance(params_mark, int):
            param_dict = self.interface_info[params_mark]
        else:
            logging.error("参数传递错误，仅支持整型和字符串类型，错误参数为：{}".format(params_mark))
        return param_dict


if __name__ == '__main__':
    ...
