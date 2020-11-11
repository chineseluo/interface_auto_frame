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
import jmespath
import requests
import logging
from models.consolelog import log_output
from models.models import OSTRespData, OSTReqData, OSTReqRespData, MethodEnum, OSTReqArgv
from Common.FileOption.yamlOption import YamlFileOption

# 读取Conf下的conf.yml全局配置文件
conf_yaml_path = os.path.join(os.path.dirname(__file__).split("Base")[0], "Conf/conf.yml")
# 根据读取的conf.yml中的配置信息获取测试的网址服务等信息
conf_server_info = YamlFileOption.read_yaml(conf_yaml_path)["server_info"]


class BaseRequest:
    """
    封装requests库中常用的四种请求方式，通过提供一个公共方法，根据yaml中的get/post/delete/put进行判断，调用不同的私有方法
    """

    def __init__(self):
        # 获取base_url
        self.__base_url = conf_server_info["protocol"] + '://' + conf_server_info["base_url"]
        # 是否开启SSL验证
        self.__verify = conf_server_info["verify"]

    @staticmethod
    def __get(url, params=None, jmespath_rule=None, **kwargs):
        logging.info(url)
        logging.info(params)
        if jmespath_rule:
            get_result = jmespath.search(jmespath_rule, requests.get(url=url, params=params, **kwargs).json())
        else:
            logging.info("进入get")
            get_result = requests.get(url=url, params=params, **kwargs)
        return get_result

    @staticmethod
    def __delete(url, jmespath_rule=None, **kwargs):
        if jmespath_rule:
            delete_result = jmespath.search(jmespath_rule, requests.delete(url=url, **kwargs).json())
        else:
            delete_result = requests.delete(url=url, **kwargs)
        return delete_result

    @staticmethod
    def __put(url, data=None, jmespath_rule=None, **kwargs):
        if jmespath_rule:
            put_result = jmespath.search(jmespath_rule, requests.put(url=url, data=data, **kwargs).json())
        else:
            put_result = requests.put(url=url, data=data, **kwargs)
        return put_result

    @staticmethod
    def __post(url=None, data=None, json=None, jmespath_rule=None, **kwargs):
        print(data)
        if jmespath_rule:
            post_result = jmespath.search(jmespath_rule, requests.post(url=url, data=data, json=json, **kwargs).json())
        else:
            post_result = requests.post(url=url, data=data, json=json, **kwargs)
        return post_result

    def send_request(self, part_url, method, send_params=None, send_data=None, send_json=None,
                     **kwargs) -> OSTReqRespData:
        """
        Choose different processing logic according to the method of transfer
        :param part_url:
        :param method:
        :param send_params:
        :param send_data:
        :param send_json:
        :param kwargs:
        :return:
        """
        result = None
        if method == MethodEnum.GET:
            result = self.__get(params=send_params, url=self.__base_url + part_url, verify=self.__verify, **kwargs)
        elif method == MethodEnum.POST:
            result = self.__post(data=send_data, json=send_json, url=self.__base_url + part_url, verify=self.__verify,
                                 **kwargs)
        elif method == MethodEnum.DELETE:
            result = self.__delete(url=self.__base_url + part_url, verify=self.__verify, **kwargs)
        elif method == MethodEnum.PUT:
            result = self.__put(data=send_data, url=self.__base_url + part_url, verify=self.__verify, **kwargs)
        else:
            logging.error("请传递正确的请求方法参数！当前错误参数为：{}".format(method))
        ost_req = OSTReqData(
            method=result.request.method,
            url=result.request.url,
            headers=result.request.headers,
            cookies=result.request._cookies,
            body=result.request.body
        )
        log_output(ost_req, "request")
        ost_resp = OSTRespData(
            status_code=result.status_code,
            cookies=result.cookies,
            encoding=result.encoding,
            headers=result.headers,
            content_type=result.headers.get("content-type"),
            body=result.content
        )
        log_output(ost_resp, "response")
        ost_rep_resp = OSTReqRespData(
            request=ost_req,
            response=ost_resp
        )
        logging.info(f"输出对象{ost_rep_resp}")
        return ost_rep_resp


if __name__ == '__main__':
    ...
