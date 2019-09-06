# coding: utf-8
# @author linpan

import json
import requests
from datetime import datetime
from random import randint

from hashlib import md5
from config import INSTMID, TID, MD5, MID, msgSrcId, MSGSRC, P_URL, T_URL
from exception import AumsValueError, AumsPayValidationError


class ChinaAumsPay:
    """
    银联商务Python SDK接口
    默认md5加密

    """

    def __init__(self,
                 notify_url=None,
                 return_url=None,
                 wallet_option="SINGLE",
                 msg_type="bills.getQRCode",
                 debug=True):

        self.wallet_option = wallet_option
        self.inst_mid = INSTMID
        self.msg_type = msg_type  # 消息类型
        self.mid = MID  # 商家号
        self.tid = TID  # 终端号
        self.msg_src_id = msgSrcId
        self.msg_src = MSGSRC
        self.md5 = MD5

        if debug is True:
            self.api_url = T_URL
        else:
            self.api_url = P_URL

    def build_body(self, extra_context=None, notify_url=None, return_url=None):
        """
        报文的公共部分
        :param extra_context:
        :param notify_url:
        :param return_url:
        :return:
        """

        request_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bill_date = datetime.now().strftime("%Y-%m-%d")
        context = {
            "mid": self.mid,
            "tid": self.tid,
            "instMid": self.inst_mid,
            "msgType": self.msg_type,
            "msgSrc": self.msg_src,
            "requestTimestamp": request_timestamp,
            "billDate": bill_date,
            "billNo": self._bill_no
        }

        if return_url is not None:
            context['return_url'] = return_url

        if notify_url is not None:
            context['notify_url'] = notify_url
        if extra_context is not None:
            context.update(extra_context)
        return context

    def make_sign(self, params):
        """构建签名"""

        sorted_params = self.build_order_param(params=params)
        sign_string = self.build_sign_string(sorted_params)
        # unicode string 不支持
        if isinstance(sign_string, unicode):
            sign_string = sign_string.encode('utf-8')

        md5_key = md5(sign_string).hexdigest().upper()
        print (md5_key)
        return md5_key

    def build_order_param(self, params):
        """
        把数组所有元素，按照“参数=参数值”的模式用“&”字符拼接成字符串
        :param params:
        :return:
        """

        params.pop('sign', None)

        # 处理混合格式 list or dict 序列号
        mix_data_type = []

        for key, value in params.iteritems():
            if isinstance(value, list):
                mix_data_type.append(key)

        for key in mix_data_type:
            params[key] = json.dumps(params[key])

        sort_params = sorted(
            [(key, value) for key, value in params.iteritems()], key=lambda x: x[0])
        return sort_params

    def build_sign_string(self, sort_param):
        """
        把字段=&连接,最后加上通讯md5
        :param sort_param:
        :return:
        """

        results = []
        for item in sort_param:
            results.append("%s=%s" % (item[0], item[1]))

        sign_string = '&'.join(results)
        return sign_string + self.md5

    def check_sign(self, params, sign):
        """
        验证签名
        :return:
        """
        sign_check = self.make_sign(params)
        return sign == sign_check

    @property
    def _bill_no(self):
        """
        #商户订单号生产
        # 组成 前缀（2）+ 时间(17)+随机数(5)
        :param :
        :return:
        """
        date = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
        rand_int = ''.join([str(randint(0, 9)) for _ in range(0, 7)])
        return self.msg_src_id + date + rand_int

    def get_qrcode(
            self,
            total_amount,
            bill_desc='拍卖会保证金',
            extra_context=None,
            notify_url=None,
            return_url=None):
        """

        :param extra_context: min=1,添加其他额外字段 type: dict
        :param total_amount: 金额必须是字符数字
        :param bill_desc: 不超过128个汉字
        :param notify_url:
        :param return_url:
        :return:
        """

        extra_fields = {"billDesc": bill_desc,
                        "totalAmount": total_amount,
                        }

        if extra_context is not None:
            if isinstance(extra_context, dict):
                extra_context.update(extra_context)
        context = self.build_body(
            extra_context=extra_fields,
            notify_url=notify_url,
            return_url=return_url)

        # 获得完整的请求字段
        key_md5 = self.make_sign(context)
        context['sign'] = key_md5
        res = requests.post(self.api_url, data=json.dumps(context))

        return self._verify_and_return_sync_response(res, self.msg_type)

    def _verify_and_return_sync_response(self, response, response_msg_type):
        """
        确保返回的消息签名验证正确, 防止篡改消息体
        return response if verification succeeded, raise exception if not
        :param response:
        :param response_msg_type: msg_type
        :return:
        """
        res = json.loads(response.text)
        if 'sign' not in res.keys():
            raise AumsValueError('%s签名不存在！' % response_msg_type)

        if res['msgType'] != self.msg_type:
            raise AumsValueError('%s请求消息类型不对！' % response_msg_type)

        sign = res['sign']
        if not self.check_sign(res, sign):
            raise AumsPayValidationError('签名不匹配!')

        return response


if __name__ == '__main__':

    up = ChinaAumsPay()

    data ={u'billNo': u'3194201909051048400795928430', u'billDate': u'2019-09-05', u'mid': u'898340149000005', u'errCode': u'SUCCESS', u'responseTimestamp': u'2019-09-05 10:48:40', u'msgType': u'bills.getQRCode', u'qrCodeId': u'10001909052754840109799410', u'instMid': u'QRPAYDEFAULT', u'tid': u'88880001', u'msgSrc': u'WWW.TEST.COM', u'sign': u'59D9AB858037B79C32536027747E99E6', u'errMsg': u'\u67e5\u8be2\u4e8c\u7ef4\u7801\u6210\u529f', u'billQRCode': u'https://qr-test2.chinaums.com/bills/qrCode.do?id=10001909052754840109799410'}

    print (up.check_sign(data, '59D9AB858037B79C32536027747E99E6'))