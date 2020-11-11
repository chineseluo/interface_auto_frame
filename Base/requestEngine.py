#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : interface_auto_frame
@Time    : 2020/10/12 11:28
@Auth    : chineseluo
@Email   : 848257135@qq.com
@File    : requestEngine.py
@IDE     : PyCharm
------------------------------------
"""
import logging
import re
from typing import Text, List, Dict, Tuple
import jmespath
from models.models import OSTReqRespData, OSTReqArgv
from .baseRequest import BaseRequest


def check_assertion(res, checker):
    """
    根据checker传入的对象进行数据提取，checker可能是一个嵌套列表，嵌套元组
    :param res:
    :param checker:
    :return:
    """
    if isinstance(checker[0], (List, Tuple)):
        for assert_item in checker:
            extract_resp = jmespath.search(res, assert_item[0])
            if assert_item[1]:
                try:
                    assert extract_resp == assert_item[1]
                except AssertionError:
                    logging.error(f"Assert Fail,Expected Value：{assert_item[1]},Response Data：{res}")
            else:
                logging.error(f"Assert Fail,Get Assert Object Fail：{assert_item}")
                raise AssertionError
    elif isinstance(checker, Text):
        extract_resp = jmespath.search(res, checker[0])
        try:
            assert extract_resp == checker[1]
        except AssertionError:
            logging.error(f"Assert Fail,Expected Value：{checker[1]}，响应数据：{res}")
            raise AssertionError
    else:
        logging.error(f"请输入正确的检查器参数，仅支持list or tuple，错误参数为：{checker}")


def url_replace(url: Text, url_converter) -> Text:
    """
    用于对URL中的&参数进行转换
    :param url:
    :param url_converter:
    :return:
    """
    replace_url = url
    if isinstance(url_converter, (List, Tuple)):
        for item in url_converter:
            replace_url = re.sub("[$]", item, replace_url, count=1)
    elif isinstance(url_converter, Text):
        replace_url = url.replace("$", url_converter)
    else:
        logging.error(f"请输入正确的参数器参数，仅支持list or tuple，错误参数为：{url_converter}")
    return replace_url


def start_run_case(params_object, params_mark, session_connection=None, checker=None, params=None, data=None,
                   json=None, files=None, url_converter=None, **kwargs) -> OSTReqRespData:
    # 注入请求对象
    params_obj = params_object()
    params_dict = params_obj.get_param_by_yaml(params_mark)
    req = BaseRequest()
    logging.info(params_dict)
    # 注入请求数据
    if session_connection:
        params_dict['header'].update(session_connection)
    if url_converter:
        part_url = url_replace(params_dict['url'], url_converter)
    else:
        part_url = params_dict['url']
    if params:
        params_dict['params'].update(params)
    if data:
        params_dict['data'].update(data)
    if json:
        params_dict['json'].update(json)
    if files:
        params_dict['files'].update(files)
    # receive a request and response object
    logging.info(params_dict['params'])
    ost_req_argv = OSTReqArgv(
        part_url=part_url,
        method=params_dict['method'].upper(),
        params=params_dict['params'],
        data=params_dict['data'],
        json=params_dict['json'],
        headers=params_dict['headers'],
        **kwargs
    )
    logging.info(ost_req_argv)
    ost_rep_resp = req.send_request(part_url=part_url, method=params_dict['method'].upper(),
                                    send_params=None, send_data=params_dict['data'],
                                    send_json=params_dict['json'], headers=params_dict['headers'], **kwargs)
    if checker:
        # 根据jmespath_rule和对比值进行判断，需要支持多重判断
        check_assertion(ost_rep_resp.response, checker)
    print(type(ost_rep_resp))
    return ost_rep_resp


if __name__ == "__main__":
    ...