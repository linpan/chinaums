# coding:utf-8
# 全民付移动c扫b 接口公共参数配置

# 编码类型
ENCODE = "UTF-8"

# 测试地址test
T_URL = "https://qr-test2.chinaums.com/netpay-route-server/api/bills/qrCode.do?"
# 生产回家product
P_URL = "https://qr.chinaums.com/netpay-route-server/api/bills/qrCode.do"

# 通讯秘钥key
MD5 = "fcAmtnx7MwismjWNhNKdHC44mNXtnEQeJkRrhKJwyrW2ysRR"

# 商户号mid
MID = "898340149000005"
# 终端号tid
TID = "88880001"

# 机构商户号instMid
INSTMID = "QRPAYDEFAULT"

MSGSRC = "WWW.TEST.COM"

# 商户需自行生成billNo。此时billNo需要符合银商规范，以银商分配的4位来源编号（msgSrcId）作为账单号的前4位, 确保订单的唯一性
msgSrcId = "3194"

# 消息类型:获取二维码
msgType_getQRCode = "bills.getQRCode"

msgType_query = "bills.query"

# 消息类型:关闭二维码
msgType_closeQRCode = "bills.closeQRCode"

