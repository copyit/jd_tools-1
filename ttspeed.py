#!/usr/bin/env python3
# coding=utf-8
# 天天加速
import requests, json, time
from models import Account
from tools import Gtime
import logging
import argparse

headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'user-agent': 'jdapp;iPhone;8.2.6;13.1.2',
        'accept-language': 'zh-cn',
        'referer': 'https://h5.m.jd.com/babelDiy/Zeus/25Yef2fUB9QQzrGCxfWLfmkMBhDc/index.html',
    }


def valid_mobile_cookie(cookie_dict):
    headers = {
        'Referer': 'https://home.m.jd.com/myJd/newhome.action',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }
    response = requests.get('https://wq.jd.com/user/info/QueryJDUserInfo?sceneval=2', headers=headers,
                            cookies=cookie_dict)
    return response.json()['base']['nickname']


# 查询燃料
def get_energy(cookie, info=None):
    params = (
        ('source', 'game'),
        ('_', Gtime()),
    )

    response = requests.get('https://lapi.jd.com/game/getUserEnergyList', headers=headers, params=params, cookies=cookie)
    logging.info(response.json())
    return response.json()['data']


# 使用燃料
def use_energy(cookie, id):
    params = (
        ('source', 'game'),
        ('energy_id', id),
        ('_', Gtime()),
    )

    response = requests.get('https://lapi.jd.com/game/runEnergy', headers=headers, params=params, cookies=cookie)
    logging.info(response.json())


# 活动列表
def get_activity_list(cookie, info=None):
    params = (
        ('source', 'game'),
        ('_', Gtime()),
    )
    response = requests.get('https://lapi.jd.com/game/energyList', headers=headers, params=params, cookies=cookie)
    logging.info(response.json())
    return response.json()['data']


# 做活动
def do_active(cookie, id):
    params = (
        ('source', 'game'),
        ('energy_id', str(id)),
        ('url', 'undefined'),
        ('_', Gtime()),
    )
    response = requests.get('https://lapi.jd.com/game/doEnergyTask', headers=headers, params=params, cookies=cookie)
    logging.info(response.json())


# 开始任务
def start_task(cookie, task_id):
    params = (
        ('source', 'game'),
        ('source_id', str(task_id)),
        ('_', Gtime()),
    )

    response = requests.get('https://lapi.jd.com/game/startTask', headers=headers, params=params, cookies=cookie)
    logging.info(response.json())


# 获取用户信息
def get_user_info(cookie, info=None):
    params = (
        ('source', 'game'),
        ('_', Gtime()),
    )
    response = requests.get('https://lapi.jd.com/game/getUserTask', headers=headers, params=params, cookies=cookie)
    logging.info(response.json())
    return response.json()['data']


# 智能使用燃料
def smart_use_energy(cookie, info=None):
    loop = True
    while loop:
        energies = get_energy(cookie)
        if not energies:
            break
        resp = get_user_info(cookie)
        distance = resp['distance'] - resp['done_distance']
        for energy in energies:
            if energy['value'] < distance:
                use_energy(cookie, energy['id'])
                break
            loop = False


# 检查并开始任务
def check_and_start_task(cookie, info=None):
    resp = get_user_info(cookie)
    if resp['task_status'] == 0:
        start_task(cookie, resp['source_id'])


# 检查并完成活动
def check_and_done_activity(cookie, info=None):
    active = get_activity_list(cookie)
    active = filter(lambda item: item['thaw_time'] == 0, active)
    for item in list(active):
        do_active(cookie, item['id'])


def once_task(cookie, info=None):
    check_and_done_activity(cookie)
    check_and_start_task(cookie)
    smart_use_energy(cookie)


def test(cookie, info=None):
    use_energy(cookie, '9f6d5582-2f4f-4a1b-b7e8-d25cb444aade')


if __name__ == '__main__':
    func = {
        "every": once_task,
        "test": test,
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