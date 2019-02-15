## 已解决的痛点
1、pageobject分层时,page的组织和层级  
2、元素定位:通过父节点找子节点、通过子节点确定父节点、找兄弟节点  
3、多设备分配测试任务运行  
4、断言相关  
5、日志和报告  
6、业务复用和维护  


## 需要安装的
```brew install allure-commandline``` （生成allure报告的工具）  

安装requment.txt里面的第三方包

```
selenium==3.14.1
Appium-Python-Client
PyYAML
pytest
allure-pytest
flaky
pytest-sugar
```
## 常用命令
```
adb devices
adb kill-server
adb shell "dumpsys window w | grep name="  (获取当前页面的Activity)
```
运行appium服务器（带有日志形式,no-reset形式,多设备时指定连接设备）

```appium --address 0.0.0.0 --port 4723 --log "appium.log" --log-timestamp --local-timezone  --no-reset  --session-override  -U 192.168.56.101:5555```


# 快速使用

### 检测环境：
在apk中添加要测的app包  
运行env_check.py检测环境  

### 原理讲解
**0：分层概念**  
page集、page类、page类加载方法（load_android、load_ios）、page元素、元素的属性  
**1、配置文件**  
路径: 项目/data/config_android.yaml  
需要修改的有：app包路径、appium版本号、devices相关、报告相关路径  
**2、编写pages**   
 路径： 项目/pages  
**创建一个page集合**，在pageset.py中创建page集合类然后添加类属性page类（page类名为中文，通过注册从而使page类的变量名变成中文）  
注释：最好在page集合类中添加page的层级关系的注释  

```
#pageset.py
from .productpage import *

class ProductPages:
    特卖首页=HomePage()
    分类列表搜索页=CategoryListPage()        #上级页为 特卖首页
    搜索后列表页=SearchListPage()             #上级页为 分类列表搜索页
    商品详情页=ProductDetailsPage()
```

**创建page类**(继承basepage类)，必填属性：name ，实现基类方法：load_android、load_ios （先不用这个） 
 
**load_android格式**：  
 ```
#productpage.py
from base.page import BasePage,get_locator

class CategoryListPage(BasePage):

    name="分类列表搜索页"

    def load_android(self):
        self.activity="com.jumei.list.category.CategoryListActivity"

        self.搜索输入框=get_locator(self.name,"搜索输入框",'id','com.jm.android.jumei:id/search_input')
        self.搜索按钮=get_locator(self.name,"搜索按钮",'id','com.jm.android.jumei:id/search_bt')
```
get_locator方法返回元素实例（dict），元素包含有属性：page名、元素名、元素定位方式、定位参数、是否是动态（默认为静态），传参时一般只需要传page名、元素名、元素定位方式、定位参数  

**3、编写用例**： 
路径： 项目/test/test_用例组名.py  
**上下文**：  
默认必有py文件 **conftest***，这是pytest运行时的上下文环境（setup、teardown）,导入的base.conftest  
原理通过pytest.fixture装饰器从而不同作用域下实现setup、teardown， 
已加载 初始化环境、driver的运行环境、用例日志  

用例组文件下编写用例集合类(test_用例集名)，编写用例方法（test_用例名）  

**基础用例**：  
```
#test_home.py
from base.action import ElementActions
from pages.pageset import ProductPages as p
from base.utils import log

class TestLogin():


    def test_home(self, action: ElementActions):

        action.sleep(8)

        action.start_activity(p.特卖首页.activity)\
            .sleep(4)\
            .click(p.特卖首页.搜索输入框)

        action.text(p.分类列表搜索页.搜索输入框,"迪奥口红")\
            .click(p.分类列表搜索页.搜索按钮)

        action.click(p.搜索后列表页.第一个商品项)
        for count in range(20):
            if action.swip_down().is_text_displayed("商品参数"):
                break

        if action.is_text_displayed("迪奥") ==False:
            raise NotFoundTextError
        action.sleep(1)
```


**action封装方法原理**：  
click实际就是传入 页面元素参数 ，通过driver.find_element找到后再执行点击事件  
text 通过driver.find_element找到后再执行send_key  
swip_down向下滑动  
is_text_displayed : 判断当前页面是否有对应传参文本  

## 运行方式： 
1、直接运行run.py  
2、run all case:  
    ```python3 run.py```  
run one module case:   
    ```python3 run.py test/test_home.py```  
run case with key word:  
    ```python3 run.py -k <keyword>```  
run class case:  
    ```python3 run.py  test/test_demo.py::Test_demo```  
run class::method case:  
    ```python3 run.py  test/test_demo.py::Test_demo::test_home```  

### 待完善
ios兼容
