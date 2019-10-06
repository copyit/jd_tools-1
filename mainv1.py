#!/usr/bin/env python3
# coding=utf-8
# 东东果园
import requests, json, time
from models import Account
import logging
from urllib import parse
from tools import Gtime
import argparse



def valid_mobile_cookie(cookie_dict):
    headers = {
        'Referer': 'https://home.m.jd.com/myJd/newhome.action',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }

    response = requests.get('https://wq.jd.com/user/info/QueryJDUserInfo?sceneval=2', headers=headers,
                            cookies=cookie_dict)
    return response.json()['base']['nickname']

def test(cookie, info=None):
    headers = {
        #'': 'authority: api.m.jd.com',
        #'cookie': 'pin=jd_4a2970c6c6b09;wskey=AAJdk-RiAEDRxYY6D9ziTm1ZU8m6TZOX9d5ueDsvvFyOzwS0e3Ml0egcU_YEdfT6Kwdwxa6TJxLxQkBsWDtrN50qHbm6J6Wy;whwswswws=xXFBtU5DNnnoS0ZzCRTh57OSTJoyxrXFgZGKdf59nDaHlOPjI9TkBg/YV8SMPRR2E8uIQYTPPIIoqgk3QSdTjeA==;unionwsws={"jmafinger":"xXFBtU5DNnnoS0ZzCRTh57OSTJoyxrXFgZGKdf59nDaHlOPjI9TkBg\\/YV8SMPRR2E8uIQYTPPIIoqgk3QSdTjeA==","devicefinger":"eidIf8c38121b2sfTitpdPT2RYezQi3M1vMzfU4rauG2wf514U0dUhOixz5SVBsO3HkC\\/VpQZdl5tjmiT+XE83JAn33wZS2sc+htiRS+51\\/1hf7za2Zl"}',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'user-agent': 'JD4iPhone/166619 (iPhone; iOS 13.1.1; Scale/3.00)',
        'accept-language': 'zh-Hans-CN;q=1',
        #'content-length': '680',
    }

    params = (
        ('functionId', 'sign'),
    )

    data = {
        #'adid': 'D20FCC8E-56EA-4FA3-87D0-99D8AF17BCE3',
        #'area': '1_2901_55554_0',
        'body': '{{"vendorId":"{id}","sourceRpc":"shop_app_sign_home"}}'.format(id='1000102825'),
        #'build': '166619',
        'client': 'apple',
        'clientVersion': '8.2.6',
        #'d_brand': 'apple',
        #'d_model': 'iPhone11,2',
        #'eid': 'eidIf8c38121b2sfTitpdPT2RYezQi3M1vMzfU4rauG2wf514U0dUhOixz5SVBsO3HkC/VpQZdl5tjmiT+XE83JAn33wZS2sc+htiRS+51/1hf7za2Zl',
        #'isBackground': 'N',
        #'joycious': '96',
        #'lang': 'en_US',
        #'networkType': 'wifi',
        #'networklibtype': 'JDNetworkBaseAF',
        'openudid': '55d32ef767c118e0963e1e145a9b9dfb247d951a',
        #'osVersion': '13.1.1',
        #'partner': 'apple',
        #'rfs': '0',
        #'scope': '01',
        #'screen': '1125*2436',
        'sign': '62cb405c91e83c4bda9466ef492b37b7',
        'st': '1570245163605',
        'sv': '112',
        #'uuid': 'coW0lj7vbXVin6h7ON+tMNFQqYBqMahr',
        #'wifiBssid': 'unknown'
    }
    data = parse.urlencode(data)
    response = requests.post('https://api.m.jd.com/client.action', headers=headers, params=params, data=data, cookies=cookie)
    logging.info(response.json())


# 双签
def double_sign(cookie, info=None):
    headers = {
        'Host': 'nu.jr.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Origin': 'https://m.jr.jd.com',
        'Accept': 'application/json',
        'User-Agent': 'jdapp;iPhone;8.2.6;13.1.1;55d32ef767c118e0963e1e145a9b9dfb247d951a;network/wifi;ADID/D20FCC8E-56EA-4FA3-87D0-99D8AF17BCE3;supportApplePay/2;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone11,2;addressid/1077100501;hasOCPay/0;appBuild/166619;supportBestPay/0;pv/90.16;apprpd/JingDou_Home;ref/https://ld.m.jd.com/userBeanHomePage/getLoginUserBean.action;psq/1;ads/;psn/55d32ef767c118e0963e1e145a9b9dfb247d951a|179;jdv/0|dmp|dmp_769|cpc|dmp_769_3059109_3C03434D7A744370ED721DB734ABF7B8_1569812439733|1569812440895|1569812443;adk/;app_device/IOS;pap/JA2015_311210|8.2.6|IOS 13.1.1;Mozilla/5.0 (iPhone; CPU iPhone OS 13_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
        'Referer': 'https://m.jr.jd.com/integrate/signin/index.html?channel=qjdicon&lng=108.553068&lat=34.066829&sid=4d824204a6eafcd765af12f164a76e6w&un_area=1_2901_55554_0',
        'Accept-Language': 'zh-cn',
    }

    params = (
        ('_', str(Gtime())),
    )

    data = 'reqData=%7B%22actCode%22%3A%22FBBFEC496C%22%2C%22type%22%3A4%2C%22riskDeviceParam%22%3A%22%7B%5C%22fp%5C%22%3A%5C%22fb6ccf86676a5be04e9ef3d17c16c5e1%5C%22%2C%5C%22eid%5C%22%3A%5C%22YVZX44NXTV27MIPV4JKUNAW3CKU7BW4Z7TZ27CJ4GUCR5U2HPY2DI7NNPANJ6BRF4KMTNLAT6DMBDMYHTASJCO44OQ%5C%22%2C%5C%22sdkToken%5C%22%3A%5C%22%5C%22%2C%5C%22sid%5C%22%3A%5C%22%5C%22%7D%22%7D'

    response = requests.post('https://nu.jr.jd.com/gw/generic/jrm/h5/m/process', headers=headers, params=params,
                             cookies=cookie, data=data)
    logging.info(response.json())


# jdjr sign
def sign_jdjr(cookie, info=None):
    headers = {
        'Host': 'ms.jr.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Origin': 'https://uf.jr.jd.com',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148/application=JDJR-App&deviceId=835406AE-A9E5-4589-9BF8-59866D34499A&clientType=ios&iosType=iphone&clientVersion=5.2.70&HiClVersion=5.2.70&isUpdate=0&osVersion=13.1.1&osName=iOS&platform=iPhone11,2&screen=812*375&src=App Store&ip=192.168.1.174&mac=02:00:00:00:00:00&netWork=1&netWorkType=1&stockSDK=stocksdk-iphone_3.2.0&sPoint=&jdPay=(*#@jdPaySDK*#@jdPayChannel=jdfinance&jdPayChannelVersion=5.2.70&jdPaySdkVersion=2.25.21.4&jdPayClientName=iOS*#@jdPaySDK*#@)',
        'Referer': 'https://uf.jr.jd.com/activities/sign/v5/index.html?channel=sqtanchuang&sid=8e7dc88bfaeeff92f18232c2fcb69b5w',
        'Accept-Language': 'zh-cn',
    }

    params = (
        ('_', str(Gtime())),
    )

    data = 'reqData=%7B%22channelSource%22%3A%22JRAPP%22%2C%22riskDeviceParam%22%3A%22%7B%5C%22deviceType%5C%22%3A%5C%22iPhone11%2C2%5C%22%2C%5C%22traceIp%5C%22%3A%5C%22%5C%22%2C%5C%22macAddress%5C%22%3A%5C%2202%3A00%3A00%3A00%3A00%3A00%5C%22%2C%5C%22imei%5C%22%3A%5C%22835406AE-A9E5-4589-9BF8-59866D34499A%5C%22%2C%5C%22os%5C%22%3A%5C%22iOS%5C%22%2C%5C%22osVersion%5C%22%3A%5C%2213.1.1%5C%22%2C%5C%22fp%5C%22%3A%5C%2214c57b0c69d0eb5bded81c693aa0012a%5C%22%2C%5C%22ip%5C%22%3A%5C%22192.168.1.174%5C%22%2C%5C%22eid%5C%22%3A%5C%22SS54IURF5FTSW753GFSKNIB4N2AGTFTLKVMGF54P2RNEW2MILXWBALJ6KK7NR47JLDLTBI5WAFOSEG3JU5GHJFL6OI%5C%22%2C%5C%22appId%5C%22%3A%5C%22com.jd.jinrong%5C%22%2C%5C%22openUUID%5C%22%3A%5C%22c6c56eae008a3a1bca1a143e9c7079bc99d30c65%5C%22%2C%5C%22uuid%5C%22%3A%5C%22%5C%22%2C%5C%22clientVersion%5C%22%3A%5C%225.2.70%5C%22%2C%5C%22resolution%5C%22%3A%5C%22812*375%5C%22%2C%5C%22channelInfo%5C%22%3A%5C%22appstore%5C%22%2C%5C%22networkType%5C%22%3A%5C%22WIFI%5C%22%2C%5C%22startNo%5C%22%3A40%2C%5C%22openid%5C%22%3A%5C%22%5C%22%2C%5C%22token%5C%22%3A%5C%22%5C%22%2C%5C%22sid%5C%22%3A%5C%22%5C%22%2C%5C%22terminalType%5C%22%3A%5C%2202%5C%22%2C%5C%22longtitude%5C%22%3A%5C%22%5C%22%2C%5C%22latitude%5C%22%3A%5C%22%5C%22%2C%5C%22securityData%5C%22%3A%5C%22%5C%22%2C%5C%22jscContent%5C%22%3A%5C%22%5C%22%2C%5C%22fnHttpHead%5C%22%3A%5C%22%5C%22%2C%5C%22receiveRequestTime%5C%22%3A%5C%22%5C%22%2C%5C%22port%5C%22%3A%5C%22%5C%22%2C%5C%22appType%5C%22%3A1%2C%5C%22optType%5C%22%3A%5C%22%5C%22%2C%5C%22idfv%5C%22%3A%5C%22%5C%22%2C%5C%22wifiSSID%5C%22%3A%5C%22%5C%22%2C%5C%22wifiMacAddress%5C%22%3A%5C%22%5C%22%2C%5C%22cellIpAddress%5C%22%3A%5C%22%5C%22%2C%5C%22wifiIpAddress%5C%22%3A%5C%22%5C%22%2C%5C%22sdkToken%5C%22%3A%5C%22WBO5IO64VANMWIXJT3OXXDYCDBVA7ZTKOUNS7EXDLXUS2OGUMFL4AHLAAFPFXDGZHMB4DOH23EA7U%5C%22%7D%22%7D'

    response = requests.post('https://ms.jr.jd.com/gw/generic/gry/h5/m/signIn', headers=headers, params=params,
                             cookies=cookie, data=data)
    logging.info(response.json())


# 转盘
def zhuanpan(cookie, info=None):
    headers = {
        #'': 'authority: api.m.jd.com',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'user-agent': 'jdapp;iPhone;8.2.6;13.1.1;55d32ef767c118e0963e1e145a9b9dfb247d951a;network/wifi;ADID/D20FCC8E-56EA-4FA3-87D0-99D8AF17BCE3;supportApplePay/2;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone11,2;addressid/1077100501;hasOCPay/0;appBuild/166619;supportBestPay/0;pv/90.12;apprpd/JingDou_Home;ref/https://ld.m.jd.com/userBeanHomePage/getLoginUserBean.action;psq/2;ads/;psn/55d32ef767c118e0963e1e145a9b9dfb247d951a|176;jdv/0|dmp|dmp_769|cpc|dmp_769_3059109_3C03434D7A744370ED721DB734ABF7B8_1569812439733|1569812440895|1569812443;adk/;app_device/IOS;pap/JA2015_311210|8.2.6|IOS 13.1.1;Mozilla/5.0 (iPhone; CPU iPhone OS 13_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
        'accept-language': 'zh-cn',
        'referer': 'https://turntable.m.jd.com/?actId=jgpqtzjhvaoym&appSource=jdhome&lng=108.553024&lat=34.066647&sid=4d824204a6eafcd765af12f164a76e6w&un_area=1_2901_55554_0',
    }

    params = (
        ('functionId', 'lotteryDraw'),
        ('body',
         '{"actId":"jgpqtzjhvaoym","appSource":"jdhome","lotteryCode":"xqe3jmmqzgmms2z3z7omuqmgwzupdjgryfo7twbcmyoa5dm6mcdkzuq2kajq2qa5hiawzpccizuck"}'),
        ('appid', 'ld'),
        ('client', 'apple'),
        ('clientVersion', '8.2.6'),
        ('networkType', 'wifi'),
        ('osVersion', '13.1.1'),
        ('uuid', '55d32ef767c118e0963e1e145a9b9dfb247d951a'),
        #('jsonp', 'jsonp_1570243970687_78873'),
    )

    response = requests.get('https://api.m.jd.com/client.action', headers=headers, params=params, cookies=cookie)
    logging.info(response.json())


# 签到
def sign(cookie, info=None):
    headers = {
        # '': 'authority: api.m.jd.com',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'user-agent': 'JD4iPhone/166619 (iPhone; iOS 13.1.1; Scale/3.00)',
        'accept-language': 'zh-Hans-CN;q=1',
        #'content-length': '918',
    }

    params = (
        ('functionId', 'signBeanIndex'),
    )

    data = 'adid=D20FCC8E-56EA-4FA3-87D0-99D8AF17BCE3&area=1_2901_55554_0&body=%7B%22jda%22%3A%22-1%22%2C%22monitor_source%22%3A%22bean_app_bean_index%22%2C%22shshshfpb%22%3A%22%22%2C%22fp%22%3A%22-1%22%2C%22eid%22%3A%22%22%2C%22shshshfp%22%3A%22-1%22%2C%22monitor_refer%22%3A%22%22%2C%22userAgent%22%3A%22-1%22%2C%22rnVersion%22%3A%224.0%22%2C%22shshshfpa%22%3A%22-1%22%2C%22referUrl%22%3A%22-1%22%7D&build=166619&client=apple&clientVersion=8.2.6&d_brand=apple&d_model=iPhone11%2C2&eid=eidIf8c38121b2sfTitpdPT2RYezQi3M1vMzfU4rauG2wf514U0dUhOixz5SVBsO3HkC/VpQZdl5tjmiT%2BXE83JAn33wZS2sc%2BhtiRS%2B51/1hf7za2Zl&isBackground=N&joycious=96&lang=en_US&networkType=wifi&networklibtype=JDNetworkBaseAF&openudid=55d32ef767c118e0963e1e145a9b9dfb247d951a&osVersion=13.1.1&partner=apple&rfs=0&scope=01&screen=1125%2A2436&sign=c306407b2ad267f5722b3c0dde3cfd7f&st=1570241811906&sv=110&uuid=coW0lj7vbXVin6h7ON%2BtMNFQqYBqMahr&wifiBssid=unknown'

    response = requests.post('https://api.m.jd.com/client.action', headers=headers, params=params, data=data, cookies=cookie)
    logging.info(response.json())


def ever_day(cookie, info=None):
    sign(cookie)
    zhuanpan(cookie)
    sign_jdjr(cookie)
    double_sign(cookie)


if __name__ == '__main__':
    func = {
        "test": test,
        "sign": ever_day,
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('--log', '-l', action='store_true', help='是否显示log')
    parser.add_argument('--user', '-u', default="", type=str, help="指定username")
    parser.add_argument('--action', '-a', default="", type=str, help="操作类型")
    args = parser.parse_args()

    LEVEL = "INFO" if args.log else "WARN"
    logging.basicConfig(level=LEVEL)
    users = Account.select()
    if args.user:
        users = users.where(Account.nick == args.user)
    userInfo = {}
    for i in users:
        cookie = {}
        try:
            cookie = json.loads(i.cookie_mobile)
        except Exception:
            pass
        if valid_mobile_cookie(cookie):
            action = func.get(args.action, func.get('test'))
            action(cookie)
        else:
            print('{} {}登录已经失效'.format(time.time(), i.nick))