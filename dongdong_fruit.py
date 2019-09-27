#!/usr/bin/env python3
# coding=utf-8
# 东东果园
import requests, json, time
from models import Account
from tools import Gtime
import logging
import argparse

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


# 进行三餐签到 "6-9", "11-14", "17-21"
def sancan_sign(cookie, info=None):
    headers = {
        'Sec-Fetch-Mode': 'cors',
        'Referer': 'https://h5.m.jd.com/active/dongdong-garden/index.html',
        'Origin': 'https://h5.m.jd.com',
        'User-Agent': 'jdapp;iPhone;8.2.6;13.1',
    }

    params = (
        ('functionId', 'gotThreeMealForFarm'),
        ('body', '{"type":0,"channel":1}'),
        ('appid', 'wh5'),
    )

    response = requests.get('https://api.m.jd.com/client.action', headers=headers, params=params, cookies=cookie)
    logging.info("三餐签到：{}".format(response.json()))

    params = (
        ('functionId', 'gotThreeMealForFarm'),
        ('body', '{"type":1,"channel":1}'),
        ('appid', 'wh5'),
    )
    response = requests.get('https://api.m.jd.com/client.action', headers=headers, params=params, cookies=cookie)
    logging.info("三餐分享：{}".format(response.json()))


# 完成广告活动任务
def do_ad_task(cookie, info=None):
    tasks = get_activity(cookie)
    tasksId = []
    for task in tasks['gotBrowseTaskAdInit']['userBrowseTaskAds']:
        tasksId.append(task['advertId'])

    headers = {
        'accept': '*/*',
        'origin': 'https://h5.m.jd.com',
        'accept-encoding': 'gzip, deflate, br',
        'user-agent': 'jdapp;iPhone;8.2.6;13.1',
        'accept-language': 'zh-cn',
        'referer': 'https://h5.m.jd.com/active/dongdong-garden/index.html'
    }

    for taskId in tasksId:
        params = (
            ('functionId', 'browseAdTaskForFarm'),
            ('body', '{{"advertId":"{}","type":0,"channel":1}}'.format(taskId)),
            ('appid', 'wh5'),
        )

        response = requests.get('https://api.m.jd.com/client.action', headers=headers, params=params, cookies=cookie)
        params = (
            ('functionId', 'browseAdTaskForFarm'),
            ('body', '{{"advertId":"{}","type":1,"channel":1}}'.format(taskId)),
            ('appid', 'wh5'),
        )
        response = requests.get('https://api.m.jd.com/client.action', headers=headers, params=params, cookies=cookie)


# 完成10次浇水任务
def done_10_water(cookie, info=None):
    params = (
        ('functionId', 'totalWaterTaskForFarm'),
        ('body', '{"version":2,"channel":1}'),
        ('appid', 'wh5'),
    )

    response = requests.get('https://api.m.jd.com/client.action', headers=headers, params=params, cookies=cookie)
    logging.info(response.json())


# 领取10次浇水任务
def do_10_water(cookie, info=None):
    activity = get_activity(cookie)
    water_times = activity['totalWaterTaskInit']['totalWaterTaskTimes']
    water_count = get_water_count(cookie)
    if water_count > (10-water_times)*10:
        for _ in range(10-water_times):
            water_fruit(cookie)
        logging.info("浇水完成")
        done_10_water(cookie)

    else:
        logging.info("水不够完成10次浇水任务")


# 获取活动信息
def get_activity(cookie, info=None):
    headers = {
        'accept': '*/*',
        'origin': 'https://h5.m.jd.com',
        'accept-encoding': 'gzip, deflate, br',
        'user-agent': 'jdapp;iPhone;8.2.6;13.1',
        'accept-language': 'zh-cn',
        'referer': 'https://h5.m.jd.com/active/dongdong-garden/index.html'
    }

    params = (
        ('functionId', 'taskInitForFarm'),
        ('body', '{"channel":1}'),
        ('appid', 'wh5'),
    )

    response = requests.get('https://api.m.jd.com/client.action', headers=headers, params=params, cookies=cookie)
    logging.info("获取活动:{}".format(response.json()))
    return response.json()


# 每日签到
def every_day_sign(cookie, info=None):
    # 签到
    params = (
        ('functionId', 'signForFarm'),
        ('body', '{"type":0,"version":2,"channel":1}'),
        ('appid', 'wh5'),
    )

    response = requests.get('https://api.m.jd.com/client.action', headers=headers, params=params, cookies=cookie)
    logging.info(response.json())

    # 分享
    params = (
        ('functionId', 'signForFarm'),
        ('body', '{"type":1,"version":2,"channel":1}'),
        ('appid', 'wh5'),
    )

    response = requests.get('https://api.m.jd.com/client.action', headers=headers, params=params, cookies=cookie)
    logging.info(response.json())


# 浇水
def water_fruit(cookie, info=None):
    headers = {
        'accept': '*/*',
        'origin': 'https://h5.m.jd.com',
        'accept-encoding': 'gzip, deflate, br',
        'user-agent': 'jdapp;iPhone;8.2.6;13.1',
        'accept-language': 'zh-cn',
        'referer': 'https://h5.m.jd.com/active/dongdong-garden/index.html'
    }


    params = (
        ('functionId', 'waterGoodForFarm'),
        ('body', '{"version":2,"channel":1}'),
        ('appid', 'wh5'),
    )

    response = requests.get('https://api.m.jd.com/client.action', headers=headers, params=params, cookies=cookie)
    logging.info(response.json())


# 完成首次浇水任务
def first_water_task(cookie, info=None):
    water_fruit(cookie)

    params = (
        ('functionId', 'firstWaterTaskForFarm'),
        ('body', '{"version":2,"channel":1}'),
        ('appid', 'wh5'),
    )

    response = requests.get('https://api.m.jd.com/client.action', headers=headers, params=params, cookies=cookie)
    logging.info(response.json())


# 获取水滴数
def get_water_count(cookie, info=None):
    headers = {
        'accept': '*/*',
        'origin': 'https://h5.m.jd.com',
        'accept-encoding': 'gzip, deflate, br',
        'user-agent': 'jdapp;iPhone;8.2.6;13.1',
        'accept-language': 'zh-cn',
        'referer': 'https://h5.m.jd.com/active/dongdong-garden/index.html'
    }

    params = (
        ('functionId', 'initForFarm'),
        ('body',
         '{"imageUrl":"","nickName":"","shareCode":"","babelChannel":"3","version":2,"channel":1}'),
        ('appid', 'wh5'),
    )

    response = requests.get('https://api.m.jd.com/client.action', headers=headers, params=params, cookies=cookie)
    logging.info(response.json())
    return response.json()['farmUserPro']['totalEnergy']

# 完成分享任务
def do_share(cookie, info=None):
    headers = {
        'accept': '*/*',
        'origin': 'https://h5.m.jd.com',
        'accept-encoding': 'gzip, deflate, br',
        'user-agent': 'jdapp;iPhone;8.2.6;13.1',
        'accept-language': 'zh-cn',
        'referer': 'https://h5.m.jd.com/active/dongdong-garden/index.html'
    }

    share_codes = {
        "special_wen": "020dce83d83044188fa9e087fb47c7d9",
        "sqlness": "a5bcfb6655b04ffc8f7262dc364a1b2d",
                   }

    for k, v in share_codes.items():
        params = (
            ('functionId', 'initForFarm'),
            ('body',
             '{{"imageUrl":"","nickName":"","shareCode":"{}","babelChannel":"3","version":2,"channel":1}}'.format(v)),
            ('appid', 'wh5'),
        )

        response = requests.get('https://api.m.jd.com/client.action', headers=headers, params=params, cookies=cookie)
        logging.info(response.json())

# 单次任务
def once_task(cookie, info=None):
    #每天一次的任务
    every_day_sign(cookie)
    do_share(cookie)
    first_water_task(cookie)
    do_ad_task(cookie)


if __name__ == '__main__':
    func = {
        "once": once_task,
        "ad": do_ad_task,
        "3": sancan_sign,
        "10": do_10_water,
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