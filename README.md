```
# 简介

接口自动化测试框架：pytest+requests+allure

## 项目结构

~~~ mermaid
graph TD
   subgraph 模块调用过程
    登录页面testcase(登录页面testcase)-->|调用|登录页面对象
    登录页面对象-->base层
    注册页面testcase(注册页面testcase)-->|调用|注册页面对象
   注册页面对象-->base层
    购买页面testcase(购买页面testcase)-->|调用|购买页面对象
   购买页面对象-->base层
    client5(模块测试case)-->|调用|PageObject层
    PageObject层-->|调用|base层((base层:基础方法))
    end
~~~



整个框架主要分为三层：Base层、PageObject层、TestCase层，采用传统的互联网的垂直架构模式。

- 元素公共操作方法封装存放在Base层
- 页面元素操作存放在第二层PageObject层，后面如果页面元素变化，直接在第二层相应的Page对象修改即可
- 测试case存放在TestCases层，主要做断言等操作

## 运行环境

运行此项目前需要进行如下操作：

1. 使用pycharm导入项目

2. 打开pycharm的terminal，切换到 requirements.txt 所在的目录下，使用如下命令 ，就能在当前的 python 环境中导入所有需要的包：

   ```
   pip install -r requirements.txt
   ```

环境说明：

- 开发工具：pycharm
- python版本：python3.8
- 测试case总入口：run.py

---

**有任何使用问题请联系我：chineseluo**

---

# 模块设计

## Base模块

封装操作元素的公共方法，以及断言方法

- assertMethod.py封装断言的方法，断言失败截图，按需自己可以进行封装
- base封装页面元素操作方法

## Common模块

封装的读取配置文件的公共方法，类似于util工具类

- publicMethod，封装公共方法，后面可能会讲一些方法分类创建不同的py模块进行管理，便于维护
- Log.py，封装日志操作方法
- logging.config.yml，logging配置文件
- file_option.py，封装文件操作方法

## Conf模块

存放全局配置文件

- config.yaml中存放全局配置文件，当前包含两个
  - allure_environment：存放allure报告中环境描述初始化文件
  - test_info：测试地址
- selenium_config.yaml：存放selenium远程分布式调用配置文件

## Grid_server模块

存放selenium-server（hub和node）启动bat脚本，以及三种selenium三种浏览器命令行参数的入口

- Selenium_server_dir中存放了3.141.0版本的selenium-server-standalone的jar包
- selenium_server中存放了在linux中启动单个hub和node的bat脚本
- selenium_run_script中存放了启动本地分布式调试的脚本

## Logs模块

用于生成日志文件

- 使用pyteset本身集成的日志插件
- 同时封装了python自带的logging模块

## PageObject模块

提取页面对象封装公共操作方法

- 使用yaml文件进行页面元素的管理
- 使用elem_params.py进行yaml文件注入，生成yaml文件对象
- 页面对象初始化页面元素对象，调用base层，封装元素操作方法

## Report模块

存放测试报告，以及测试报告的生成模板allure

- report模块使用allure进行测试报告生成

## TestCases模块

用于存放测试case

- 使用conftest.py进行页面对象注入，类似unintest的setup，teardown的操作，通过装饰器进行控制
- 测试case，页面的测试用例，根据模块来进行划分

## 其他文件说明

- `.gitlab-ci.yml`：gitlab-ci配置

- `conftest.py`：封装了本地测试driver，分布式driver方法，定义了钩子函数，进行pytest功能拓展

- `pytest.ini`：配置了pytest的日志功能，以及测试用例扫描

- `requirements.txt`：框架运行所需要的jar包

- `run.py`：本地调试入口，ci集成测试入口

---

# allure装饰器

- @allure.severity("critical")
  - 优先级，包含blocker, critical, normal, minor, trivial几个不同的等级
    - 测试用例优先级1：blocker，中断缺陷（客户端程序无响应，无法执行下一步操作）
    - 测试用例优先级2：critical，临界缺陷（ 功能点缺失）
    - 测试用例优先级3：normal，普通缺陷（数值计算错误）
    - 测试用例优先级4：minor，次要缺陷（界面错误与UI需求不符）
    - 测试用例优先级5：trivial级别，轻微缺陷（必输项无提示，或者提示不规范）'
- @allure.feature("测试模块_demo1")
  - 功能块，feature功能分块时比story大,即同时存在feature和story时,feature为父节点
- @allure.story("测试模块_demo2")
  - 功能块，具有相同feature或story的用例将规整到相同模块下,执行时可用于筛选
- @allure.issue("BUG号：123")
  - 问题标识，关联标识已有的问题，可为一个url链接地址
- @allure.testcase("用例名：测试字符串相等")
  - 用例标识，关联标识用例，可为一个url链接地址

# 环境搭建

## python安装

`version:3.8`

## java环境配置

`version 1.8`，win10系统中配置配置java环境，参考[win10java环境配置](https://www.runoob.com/w3cnote/windows10-java-setup.html)

## allure安装

- 不同平台安装allure的方法不同，这里仅介绍windows平台下allure的安装步骤。其它平台请阅读[allure官方文档](https://docs.qameta.io/allure/)进行操作
- 官方提供的安装方法可能会受网络环境影响而安装失败，可选择在[GitHub仓库](https://github.com/allure-framework/allure2 )下载文件并安装allure2
- Windows环境下可以用以下步骤进行安装
  - 安装scoop，使用**管理员权限**打开powershell窗口，输入命令`Invoke-Expression (New-Object System.Net.WebClient).DownloadString('https://get.scoop.sh')`
  - 如果安装不成功则运行`Set-ExecutionPolicy RemoteSigned -scope CurrentUser`，运行成功后重新执行第一步
  - scoop安装成功后控制台会输出`Scoop was installed successfully!`
  - 执行`scoop install allure`进行allure的安装
  - allure安装成功后控制台会输出`'allure' (2.13.1) was installed successfully!`

## selenium环境搭建

### selenium本地分布式启动和配置

第三步和第四步操作已集成脚本中，执行start_server_windows.bat即可

1. 下载selenium-server-standalone，[下载地址](http://selenium-release.storage.googleapis.com/index.html)，需要对应自己本地的selenium版本
2. 下载对应的浏览器的driver，放置到python的安装目录
   - [Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads)
   - [Firefox](https://github.com/mozilla/geckodriver/releases)
   - [IE](http://selenium-release.storage.googleapis.com/index.html?path=3.5/)
3. 启动hub节点（管理节点负责任务的分发，数据收集统计）`java -jar selenium-server-standalone-3.5.0.jar -role hub`（ps:端口可以修改）
4. 启动node节点`java -jar selenium-server-standalone-3.5.0.jar -role node -port 5555 -hub http://localhost:4444/grid/register`（ps:端口可以修改，需要启用多少个node节点，只需要修改port即可）

# 如何编写测试用例

下面详细说明如何添加一条用例，以登录界面演示

1. 在PageObject下Login_page模块新建一个页面元素yaml文件，Login_page.yaml

   字段说明：

   - desc：yaml文件说明
   - parameters：参数说明
   - elem_name：元素别名（你调用的时候需要使用）
   - desc：元素描述（例如用户输入框的名称）
   - data：里面是一个字典，元素定位方式，以及元素定位方式的取值

   ```yaml
   #封装需要操作的元素对象
   desc: "登录页面元素操作对象"
   parameters:
     - elem_name: "Username"
       desc: "用户输入框名称"
       data: {
         method: "NAME",
         value: "Username"
       }
   
     - elem_name: "Password"
       desc: "密码输入框名称"
       data: {
         method: "NAME",
         value: "Password"
       }
   ```

   

2. 在PageObject模块下的elem_params.py文件中进行Login_page.yaml注册，生成一个yaml文件对象，初始化传递两个参数，一个是模块名，一个是yaml配置文件名

   ```yaml
   # 注册yaml文件对象
   class LoginPageElem(ElemParams):
       def __init__(self):
           super(LoginPageElem, self).__init__('Login_page', 'Login_page.yaml')
   ```

3. 在PageObject下Login_page模块创建一个login_page.py封装login页面操作元素，导入Login_page.yaml文件对象，初始化，然后获取yaml文件中封装的元素，底层通过传入locator定位器（元组），进行页面元素操作

   ```python
   # !/user/bin/env python
   # -*- coding: utf-8 -*-
   # @Time    : 2020/5/12 21:11
   # @Author  : chineseluo
   # @Email   : 848257135@qq.com
   # @File    : run.py
   # @Software: PyCharm
   from Base.base import Base
   from selenium import webdriver
   from PageObject.elemParams import Login_page_elem
   
   
   # 封装速涡手游加速器登录页面操作对象操作方法
   class LoginPage(Base):
       def __init__(self, driver):
           # 初始化页面元素对象，即yaml文件对象
           self.elem_locator = Login_page_elem()
           # 初始化driver
           super().__init__(driver)
   
       def login_by_config_url(self):
           """
               从配置文件config.yaml获取登录地址
           @return: 登录地址
           """
           return super().login_by_config_url()
   
       def get_username_attribute_value(self):
           """
               获得账号输入框的placeholder值
           @return: 获得账号输入框的placeholder值
           """
           elem = self.elem_locator.get_locator("Username")
           return super().get_placeholder(elem)
   
       def get_password_attribute_value(self):
           """
               获得密码输入框的placeholder值
           @return:获得密码输入框的placeholder值
           """
           elem = self.elem_locator.get_locator("Password")
           return super().get_placeholder(elem)
   ```

4. 在TestCases下面新建一个包，例如Login模块，测试登录页面

5. 在Login下面创建一个conftest.py和test_login_page_case.py

   conftest.py中指定需要加载的测试页面对象，使用scope级别为function

   ```python
   import pytest
   from PageObject.Login_page.loginPage import LoginPage
   
   
   @pytest.fixture(scope="function")
   def login_page_class_load(function_driver):
       login_page = LoginPage(function_driver)
       yield login_page
   ```

   test_login_page_case.py中每个测试case需要调用页面模块conftest.py中的function，以及全局配置conftest.py中function_driver（或者function_remote_driver，分布式需要使用该参数)，断言使用Base模块中的assert_method的Assert_method，里面封装了断言方法，包含了allure断言失败截图等操作，根据不同的断言场景取用，或者自己再进行封装

   ```python
   # coding:utf-8
   import pytest
   import allure
   import inspect
   import logging
   from Base.assertMethod import AssertMethod
   
   
   @allure.feature("Login_page_case")
   class TestLoginPageCase:
   
       @allure.story("Login")
       @allure.severity("normal")
       @allure.description("测试登录")
       @allure.link("https://www.baidu.com", name="连接跳转百度")
       @allure.testcase("https://www.sina.com", name="测试用例位置")
       @allure.title("执行测试用例用于登录模块")
       def test_DLZC1(self, login_page_class_load, function_driver):
           logging.info("用例编号编码：{}".format(inspect.stack()[0][3]))
           login_page_class_load.login_by_config_url()
           username_input_attribute_value = login_page_class_load.get_username_attribute_value()
           AssertMethod.assert_equal_screen_shot(function_driver, (username_input_attribute_value, "手机号码"))
   ```

6. 执行用例

   执行用例可以通过两种常用的方法进行

   1. pycharm中配置`test runner`为`pytest`，配置路径为`settings->Tools->Python Integrated Tools->Testing`；配置完成后就能够在打开测试用例文件后看到可执行的按钮了

   2. 在根目录下的`run.py`文件中运行，需要配置要运行的`Fixture`后就可以运行了。例如当你在调试`Login`时只需要保证`allure_features_list`中只有`Login`就行了，`pytest`会自动寻找`Fixture`值为`Login`参数的用例

      ```python
      allure_features_list = [
          'Register_page_case',
          'Login_page_case'
      ]
      ```

      


```

# requests几种传递参数的区别：
params:字典或者字节序列，作为参数添加到URL中，即params是往URL后面添加参数，存在于requests.get中
body:传递的消息体，里面通常是data和json
data:消息体的一种格式，字典格式
json:消息体的一种格式，json格式
