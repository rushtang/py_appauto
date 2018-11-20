



from .productpage import *
from .userpage import *
from base.utils import Conf


#用户中心相关Page集合类
class UserPages:
    登录页=LoginPage()



#商品page集合类（商品主干流程相关的）
class ProductPages:
    特卖首页=HomePage()
    分类列表搜索页=CategoryListPage()        #上级页为 特卖首页
    搜索后列表页=SearchListPage()             #上级页为 分类列表搜索页
    商品详情页=ProductDetailsPage()





