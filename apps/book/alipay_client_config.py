from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from decouple import config

alipay_client_config = AlipayClientConfig()

alipay_client_config.server_url = config('ALIPAY_CLIENT_CONFIG_SERVER_URL', default='https://openapi.alipaydev.com/gateway.do')
alipay_client_config.app_id = config('ALIPAY_CLIENT_CONFIG_APP_ID', default='2016090900473485')
alipay_client_config.app_private_key = config('ALIPAY_CLIENT_CONFIG_APP_PRIVATE_KEY', default='')
alipay_client_config.alipay_public_key = config('ALIPAY_CLIENT_CONFIG_ALIPAY_PUBLIC_KEY', default='')
alipay_client_config.charset = config('ALIPAY_CLIENT_CONFIG_CHARSET', default='UTF8')
alipay_client_config.sign_type = config('ALIPAY_CLIENT_CONFIG_SIGN_TYPE', default='RSA2')


