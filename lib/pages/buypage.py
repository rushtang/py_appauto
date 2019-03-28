from base.page import BasePage
from base.action import ElementActions
from base.utils import log




class BuySettlementPage(BasePage):

    name="结算页"


    def load_android(self):

        self.结算价格=self.get_locator("结算价格",'id','com.jm.android.jumei:id/tv_PayTotoalPrice')
        self.提交订单=self.get_locator("提交订单",'id','com.jm.android.jumei:id/gosubmit_order')

        self.购买数量增加=self.get_locator('购买数量增加','id','com.jm.android.jumei:id/product_num_add')
        self.购买数量减少=self.get_locator('购买数量减少','id','com.jm.android.jumei:id/product_num_lower')

        self.现金卷是否可用=self.get_locator('现金卷是否可用','id','com.jm.android.jumei:id/pco_unuse_num')
        self.红包是否可用=self.get_locator('红包是否可用','id','com.jm.android.jumei:id/redpaket_use_num')

        self.使用现金卷=self.get_locator('使用现金卷','id','com.jm.android.jumei:id/pco_useBtn')
        self.使用红包=self.get_locator('使用红包','id','com.jm.android.jumei:id/use_redpaket_btn')



class PayOrderPage(BasePage):
    name = "支付订单页"

    def load_android(self):
        self.订单金额=self.get_locator('订单金额','id','com.jm.android.jumei:id/order_price')
        self.去支付=self.get_locator('去支付','id','com.jm.android.jumei:id/gosubmit_pay')
        self.支付方式选择s=self.get_locator('支付方式选择s','id','com.jm.android.jumei:id/payment_cod_btn') #有多个,按顺序为 支付宝、微信支付

        # 放弃付款弹窗内的
        self.去意已决 = self.get_locator('去意已决', 'id', 'com.jm.android.jumei:id/cancel')
        self.再想想 = self.get_locator('再想想', 'id', 'com.jm.android.jumei:id/ok')


class PayresultPage(BasePage):
    name = '支付结果页'




class MyOrderPage(BasePage):
    name = "我的订单页"


    def load_android(self):
        self.交易单号=self.get_locator('交易单号','id','com.jm.android.jumei:id/order_id')  #text属性格式：	"交易单号 c267608325"


        #订单项相关
        self.订单商品项s=self.get_locator('订单商品项s','id','com.jm.android.jumei:id/root_layout')  #有多个
        self.订单商品单价格s=self.get_locator('订单商品单价格s','id','com.jm.android.jumei:id/item_price') #有多个
        self.立即支付s=self.get_locator('立即支付s','name','立即支付')   #有多个
        #使用newlocator
        self.订单商品名=self.get_locator('订单商品名','xpath','',dynamic=True)

