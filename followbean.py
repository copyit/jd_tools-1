#!/usr/bin/env python3
# coding=utf-8
# 东东果园
import requests, json, time
from models import Account
from tools import Gtime
import logging
import argparse
from urllib import parse

headers = {
    'accept': '*/*',
    'origin': 'https://h5.m.jd.com',
    'accept-encoding': 'gzip, deflate, br',
    'user-agent': 'jdapp;iPhone;8.2.6;13.1',
    'accept-language': 'zh-cn',
    'referer': 'https://h5.m.jd.com/active/dongdong-garden/index.html'
}


def valid_mobile_cookie(cookie_dict):
    headers = {
        'Referer': 'https://home.m.jd.com/myJd/newhome.action',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }

    response = requests.get('https://wq.jd.com/user/info/QueryJDUserInfo?sceneval=2', headers=headers,
                            cookies=cookie_dict)
    return response.json()['base']['nickname']


# 查询活动
def search_active(cookie, info=None):
    headers = {
        # '': 'authority: api.m.jd.com',
        # 'cookie': 'pin=jd_4a2970c6c6b09;wskey=AAJdoWtfAECmSa38ZBJIs4y_9Db4qQ3rK0fniTRlq2YRY3MxYgeNuWm6XwSlq0rCV8gi1O4Tqr9eN72s3QzrUMikrmMFPsPJ;whwswswws=xXFBtU5DNnnoS0ZzCRTh57OSTJoyxrXFgZGKdf59nDaHlOPjI9TkBg/YV8SMPRR2E8uIQYTPPIIoqgk3QSdTjeA==;unionwsws={"jmafinger":"xXFBtU5DNnnoS0ZzCRTh57OSTJoyxrXFgZGKdf59nDaHlOPjI9TkBg\\/YV8SMPRR2E8uIQYTPPIIoqgk3QSdTjeA==","devicefinger":"eidIf8c38121b2sfTitpdPT2RYezQi3M1vMzfU4rauG2wf514U0dUhOixz5SVBsO3HkC\\/VpQZdl5tjmiT+XE83JAn33wZS2sc+htiRS+51\\/1hf7za2Zl"}',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'user-agent': 'JD4iPhone/166619 (iPhone; iOS 13.1.2; Scale/3.00)',
        'accept-language': 'zh-Hans-CN;q=1',
        # 'content-length': '913',
    }

    params = (
        ('functionId', 'getShopHomeActivityInfo'),
    )

    data = 'adid=D20FCC8E-56EA-4FA3-87D0-99D8AF17BCE3&area=1_2901_55554_0&body=%7B%22shopId%22%3A%221000224204%22%2C%22source%22%3A%22app-shop%22%2C%22latWs%22%3A%2240.085869%22%2C%22lngWs%22%3A%22116.368797%22%2C%22displayWidth%22%3A%221053.000000%22%2C%22sourceRpc%22%3A%22shop_app_home_home%22%2C%22lng%22%3A%22116.481916%22%2C%22lat%22%3A%2240.007001%22%2C%22venderId%22%3A%221000224204%22%7D&build=166619&client=apple&clientVersion=8.2.6&d_brand=apple&d_model=iPhone11%2C2&eid=eidIf8c38121b2sfTitpdPT2RYezQi3M1vMzfU4rauG2wf514U0dUhOixz5SVBsO3HkC/VpQZdl5tjmiT%2BXE83JAn33wZS2sc%2BhtiRS%2B51/1hf7za2Zl&isBackground=N&joycious=96&lang=en_US&networkType=wifi&networklibtype=JDNetworkBaseAF&openudid=55d32ef767c118e0963e1e145a9b9dfb247d951a&osVersion=13.1.2&partner=apple&rfs=0&scope=01&screen=1125%2A2436&sign=57b074b5dcd5a5e90bef65e7c068a2be&st=1570878645596&sv=121&uuid=coW0lj7vbXVin6h7ON%2BtMNFQqYBqMahr&wifiBssid=unknown'
    data = {
        'body': '{"shopId":"1000224204","source":"app-shop","latWs":"40.085869","lngWs":"116.368797","displayWidth":"1053.000000","sourceRpc":"shop_app_home_home","lng":"116.481916","lat":"40.007001","venderId":"1000224204"}',
        'client': 'apple',
        'clientVersion': '8.2.6',
        'openudid': '55d32ef767c118e0963e1e145a9b9dfb247d951a',
        'sign': '57b074b5dcd5a5e90bef65e7c068a2be',
        'st': '1570878645596',
        'sv': '121',
    }

    response = requests.post('https://api.m.jd.com/client.action', headers=headers, params=params, data=parse.urlencode(data),
                             cookies=cookie)
    logging.info(response.json())


if __name__ == '__main__':
    func = {
        "1": search_active,
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
