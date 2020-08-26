#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : interface_auto_frame
@Time    : 2020/8/26 10:00
@Auth    : chineseluo
@Email   : 848257135@qq.com
@File    : baseRequest.py
@IDE     : PyCharm
------------------------------------
"""
import os
import requests
import logging
from Common.FileOption.yamlOption import YamlFileOption


class BaseRequest:
    __conf_yaml_path = os.path.join(os.path.dirname(__file__).split("Base")[0], "Conf/conf.yml")
    __conf_server_info = YamlFileOption.read_yaml(__conf_yaml_path)["server_info"]
    __base_url = __conf_server_info["protocol"]+__conf_server_info["base_url"]
    __verify = __conf_server_info["verify"]

    def __init__(self):
        pass

    def __get(self, url, params=None, **kwargs):
        res = requests.get(url=url + self.__base_url, params=params, headers=kwargs["headers"], verify=self.__verify)
        return res

    def __delete(self, url, headers, params):
        res = requests.delete(url=url + self.__base_url, params=params, headers=headers)
        return res

    def __put(self, url, data, param_type, **kwargs):
        if param_type == "JSON":
            res = requests.put(url=url+self.__base_url, headers=kwargs["headers"], params=data, verify=self.__verify)
        elif param_type == "FORM":
            res = requests.put(url=url+self.__base_url, headers=kwargs["headers"], verify=self.__verify)
        return res

    def __post(self, url, param_type, data, json, **kwargs):
        if param_type == "JSON":
            res = requests.post(url=url + self.__base_url, headers=kwargs["headers"], params=kwargs["params"], json=json, verify=self.__verify)
        elif param_type == "FORM":
            if kwargs["files"]:
                with open(kwargs["files"], 'rb') as f:
                    file_info = {"file": f}
                    res = requests.post(url=url + self.__base_url, headers=kwargs["headers"], data=data, files=file_info, verify=self.__verify)
        else:
            res = requests.post(url=url + self.__base_url, headers=kwargs["headers"], verify=self.__verify)
        return res


if __name__ == '__main__':
    b = BaseRequest()
