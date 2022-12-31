#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import traceback

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.FileItem import FileItem
from alipay.aop.api.domain.AlipayTradeAppPayModel import AlipayTradeAppPayModel
from alipay.aop.api.domain.AlipayTradeCreateModel import AlipayTradeCreateModel
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.domain.AlipayTradePayModel import AlipayTradePayModel
from alipay.aop.api.domain.AlipayTradeQueryModel import AlipayTradeQueryModel
from alipay.aop.api.domain.AlipayTradeWapPayModel import AlipayTradeWapPayModel
from alipay.aop.api.domain.GoodsDetail import GoodsDetail
from alipay.aop.api.domain.SettleDetailInfo import SettleDetailInfo
from alipay.aop.api.domain.SettleInfo import SettleInfo
from alipay.aop.api.domain.SubMerchant import SubMerchant
from alipay.aop.api.request.AlipayOfflineMaterialImageUploadRequest import AlipayOfflineMaterialImageUploadRequest
from alipay.aop.api.request.AlipayTradeAppPayRequest import AlipayTradeAppPayRequest
from alipay.aop.api.request.AlipayTradeCreateRequest import AlipayTradeCreateRequest
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.request.AlipayTradePayRequest import AlipayTradePayRequest
from alipay.aop.api.request.AlipayTradeQueryRequest import AlipayTradeQueryRequest
from alipay.aop.api.request.AlipayTradeWapPayRequest import AlipayTradeWapPayRequest
from alipay.aop.api.response.AlipayOfflineMaterialImageUploadResponse import AlipayOfflineMaterialImageUploadResponse
from alipay.aop.api.response.AlipayTradeCreateResponse import AlipayTradeCreateResponse
from alipay.aop.api.response.AlipayTradePagePayResponse import AlipayTradePagePayResponse
from alipay.aop.api.response.AlipayTradePayResponse import AlipayTradePayResponse
from alipay.aop.api.response.AlipayTradeQueryResponse import AlipayTradeQueryResponse
from alipay.aop.api.response.AlipayTradeWapPayResponse import AlipayTradeWapPayResponse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a', )
logger = logging.getLogger('')
if __name__ == '__main__':
    # 实例化客户端
    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'
    alipay_client_config.app_id = 'your appid'
    alipay_client_config.app_private_key = 'your app private key'
    alipay_client_config.alipay_public_key = 'your app public key'
    alipay_client_config.charset = "UTF8"
    alipay_client_config.sign_type = 'RSA2'


    client = DefaultAlipayClient(alipay_client_config, logger)

    #

    # 测试统一收单下单并支付页面接口
    # model = AlipayTradePagePayModel()
    # model.out_trade_no = "202108170101010041"
    # model.total_amount = 88.88
    # model.subject = "123"
    # # model.buyer_id = "2088102177846880";
    # # model.body = "测试"
    # # model.time_expire = "10m"
    # model.product_code = "FAST_INSTANT_TRADE_PAY"
    #
    # request = AlipayTradePagePayRequest(biz_model=model)
    #
    # # request.return_url = "http://localhost:5000/trips"
    # request.return_url = ""
    # request.notify_url = ""
    #
    # # 执行API调用
    # response_content = False
    # try:
    #     response_content = client.page_execute(request)
    #     print(response_content)
    # except Exception as e:
    #     print(traceback.format_exc())
    # if not response_content:
    #     print("failed execute")
    # else:
    #     # 解析响应结果
    #     response = AlipayTradePagePayResponse()
    #     response.parse_response_content(response_content)
    #     # 响应成功的业务处理
    #     if response.is_success():
    #         # 如果业务成功，可以通过response属性获取需要的值
    #         print("get response trade_no:" + response.trade_no)
    #     # 响应失败的业务处理
    #     else:
    #         # 如果业务失败，可以从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
    #         print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)

    # 构造请求参数对象
    # model = AlipayTradeCreateModel()
    # model.out_trade_no = "20150320010101001";
    # model.total_amount = "88.88";
    # model.subject = "Iphone6 16G";
    # model.buyer_id = "2088102177846880";
    # request = AlipayTradeCreateRequest(biz_model=model)
    # # 执行API调用
    # response_content = False
    # try:
    #     response_content = client.execute(request)
    # except Exception as e:
    #     print(traceback.format_exc())
    # if not response_content:
    #     print("failed execute")
    # else:
    #     # 解析响应结果
    #     response = AlipayTradeCreateResponse()
    #     response.parse_response_content(response_content)
    #     # 响应成功的业务处理
    #     if response.is_success():
    #         # 如果业务成功，可以通过response属性获取需要的值
    #         print("get response trade_no:" + response.trade_no)
    #     # 响应失败的业务处理
    #     else:
    #         # 如果业务失败，可以从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
    #         print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)

    # 测试统一收单下单并支付页面接口
    # model = AlipayTradeWapPayModel()
    #
    # model.out_trade_no = "20210817010101004"
    # model.product_code = "QUICK_WAP_WAY"
    # model.subject = "测试商品"
    # model.total_amount = 8.88
    #
    #
    #
    # request = AlipayTradeWapPayRequest (biz_model=model)
    #
    # # request.return_url = "http://localhost:5000/trips"
    # request.notify_url = "http://localhost:5000/trips"
    # request.return_url = "http://localhost:5000/trips"
    #
    #
    # # 执行API调用
    # response_content = False
    # try:
    #     response_content = client.execute(request)
    # except Exception as e:
    #     print(traceback.format_exc())
    # if not response_content:
    #     print("failed execute")
    # else:
    #     # 解析响应结果
    #     response = AlipayTradeWapPayResponse ()
    #     response.parse_response_content(response_content)
    #     # 响应成功的业务处理
    #     if response.is_success():
    #         # 如果业务成功，可以通过response属性获取需要的值
    #         print("get response trade_no:" + response.trade_no)
    #     # 响应失败的业务处理
    #     else:
    #         # 如果业务失败，可以从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
    #         print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)

    # 测试统一收单线下交易查询接口

    model = AlipayTradeQueryModel()
    model.out_trade_no = "20220322175951549"

    request = AlipayTradeQueryRequest(biz_model=model)
    # request.return_url = "http://localhost:5000/trips"

    # request.return_url="http://localhost:5000/trips"
    # request = AlipayTradeCreateRequest(biz_model=model)
    # 执行API调用
    response_content = False
    try:
        response_content = client.execute(request)
        print(response_content)
    except Exception as e:
        print(traceback.format_exc())
    if not response_content:
        print("failed execute")
    else:
        # 解析响应结果
        response = AlipayTradeQueryResponse()
        response.parse_response_content(response_content)
        # 响应成功的业务处理
        if response.is_success():
            # 如果业务成功，可以通过response属性获取需要的值
            print("get response trade_no:" + response.trade_no)
        # 响应失败的业务处理
        else:
            # 如果业务失败，可以从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
            print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)
