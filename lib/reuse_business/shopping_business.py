from base.action import ElementActions
from base.utils import log,ArgsData
from lib.pages.set import ProductPages as p,UserPages as up
from base.verify import NotFoundElementError


def browseproduct(action:ElementActions,key='专场',position=0):
    p.搜索后列表页.pageinto(action,key)
    # 点击对应position的商品
    action.sleep(1).click_ele(action.find_ele(p.搜索后列表页.商品项标题s, is_Multiple=True)[position]).sleep(2)

    productname_ele = None
    for index in range(10):
        action.swip_down()
        tmpele = action.find_ele(p.商品详情页.商品参数列表)
        goods_value_eles = action.find_ele_child(tmpele, p.商品详情页.商品参数列表_商品参数值s, is_Multiple=True, wait=3)
        if len(goods_value_eles) > 0:
            productname_ele = goods_value_eles[0]
            break
    if productname_ele == None:
        raise NotFoundElementError

    action.get_img('商品详情页')
    productname = action.get_text_ele(productname_ele)

    return productname