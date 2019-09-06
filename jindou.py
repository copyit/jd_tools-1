#!/usr/bin/env python3
# coding=utf-8
import requests, json, time
from models import Account
from tools import Gtime
import logging
import argparse
from jd_request import unfollow_goods, unfollow_shops, get_follow_good_list, get_follow_shop_list

headers = {
    'Host': 'ms.jr.jd.com',
    'Accept': 'application/json',
    'Origin': 'https://uuj.jr.jd.com',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Referer': 'https://uuj.jr.jd.com/wxgrowing/moneytree7/index.html?channellv=sy&sid=a764905b65ead662bdc94860faa076cw',
    'Accept-Language': 'zh-CN,en-US;q=0.8',
    'X-Requested-With': 'com.jd.jrapp',
}


def valid_mobile_cookie(cookie_dict):
    headers = {
        'Referer': 'https://home.m.jd.com/myJd/newhome.action',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }

    response = requests.get('https://wq.jd.com/user/info/QueryJDUserInfo?sceneval=2', headers=headers,
                            cookies=cookie_dict)
    return response.json()['base']['nickname']


def user_info(cookie_dict):
    data = {
        'reqData': '{"shareType":1,"source":0,"riskDeviceParam":"{\\"fp\\":\\"\\",\\"eid\\":\\"\\",\\"sdkToken\\":\\"\\",\\"sid\\":\\"\\"}"}'
    }
    response = requests.post('https://ms.jr.jd.com/gw/generic/uc/h5/m/login?_={}'.format(Gtime()),
                             headers=headers, data=data, cookies=cookie_dict)
    logging.debug("login接口响应数据{}".format(response.json()))
    return (response.json()['resultData']['data'])


def shouhuo(cookie_dict, userInfo):
    # 收获金果
    data = {
        'reqData': '{{"source":2,"sharePin":null,"userId":"{}","userToken":"{}"}}'.format(userInfo['userInfo'], userInfo['userToken'])
    }

    response = requests.post('https://ms.jr.jd.com/gw/generic/uc/h5/m/harvest?_={}'.format(Gtime()),
                             headers=headers, data=data, cookies=cookie_dict)
    logging.info("harvest接口响应数据{}".format(response.json()))


def sell_fruit(cookie_dict, userInfo):
    # 卖出金果
    header = {
        'Origin': 'https://uuj.jr.jd.com',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    }

    data = 'reqData={"source":2,"sharePin":null,"riskDeviceParam":""}'
    response = requests.post('https://ms.jr.jd.com/gw/generic/uc/h5/m/sell?_={}'.format(Gtime()),
                             headers=headers, data=data, cookies=cookie_dict)
    logging.info("sell接口响应数据{}".format(response.json()))


def sign(cookie_dict, userInfo):
    # 签到
    data = 'reqData={"source":2,"workType":1,"opType":2}'

    response = requests.post('https://ms.jr.jd.com/gw/generic/uc/h5/m/doWork', headers=headers,
                             cookies=cookie_dict, data=data)
    logging.info("sign接口响应数据{}".format(response.json()))



def share(cookie_dict, userInfo):
    # 分享任务
    data = 'reqData={"source":2,"workType":2,"opType":1}'
    response = requests.post('https://ms.jr.jd.com/gw/generic/uc/h5/m/doWork', headers=headers,
                             cookies=cookie_dict, data=data)
    time.sleep(2)
    data = 'reqData={"source":2,"workType":2,"opType":2}'
    response = requests.post('https://ms.jr.jd.com/gw/generic/uc/h5/m/doWork', headers=headers,
                             cookies=cookie_dict, data=data)
    logging.info("share接口响应数据{}".format(response.json()))



def help_othres(cookie_dict, userInfo):
    sharePin = [
        'TRJqSOe2BFV5SKL6QWxIPsAdoUJQ3Dik',
        '9_F8TGySa988werHZiLH4MAdoUJQ3Dik',
    ]

    for i in sharePin:
        data = 'reqData=%7B%22sharePin%22%3A%22{}%22%2C%22shareType%22%3A%221%22%2C%22channel%22%3A%22sy%22%2C%22source%22%3A0%2C%22riskDeviceParam%22%3A%22%7B%5C%22fp%5C%22%3A%5C%22%5C%22%2C%5C%22eid%5C%22%3A%5C%22%5C%22%2C%5C%22sdkToken%5C%22%3A%5C%22%5C%22%2C%5C%22sid%5C%22%3A%5C%22%5C%22%7D%22%7D'.format(
            i)
        response = requests.post('https://ms.jr.jd.com/gw/generic/uc/h5/m/login?_='.format(Gtime()), headers=headers,
                                 cookies=cookie_dict, data=data)
        time.sleep(1)
        logging.info("help接口响应数据{}".format(response.json()))


def clean_all(cookie_dict, userInfo):
    shop_count = 0
    good_count = 0
    while True:
        goods = get_follow_good_list(cookie_dict, 1, 50)
        if not len(goods):
            break
        good_count += len(goods)
        goods = ','.join([good['commId'] for good in goods])
        unfollow_goods(cookie_dict, goods)
    while True:
        shops = get_follow_shop_list(cookie_dict, 1, 50)
        if not len(shops):
            break
        shop_count += len(shops)
        shops = ','.join([shop['shopId'] for shop in shops])
        unfollow_shops(cookie_dict, shops)
    logging.info("取消关注店铺{},取消关注商品{}".format(shop_count, good_count))


if __name__ == '__main__':
    func = {
        "help": help_othres,
        "share": share,
        "sign": sign,
        "seal": sell_fruit,
        "clean": clean_all,
        "get": shouhuo
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
        cookie_dict = {}
        try:
            cookie_dict = json.loads(i.cookie_mobile)
        except Exception:
            pass
        if valid_mobile_cookie(cookie_dict):
            userInfo[i.nick] = user_info(cookie_dict)
            action = func.get(args.action, shouhuo)
            action(cookie_dict, userInfo[i.nick])
        else:
            print('{} {}登录已经失效'.format(time.time(), i.nick))