# coding=utf-8

import requests
import argparse
import logging

headers = {
    'Origin': 'https://try.jd.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'https://try.jd.com/report-details/reportlist.action',
}


def print_report(item):
    print("-------------")
    print(item['skuName'])
    print(item['recommendation'])
    for dis in item['descriptions']:
        print(dis['content'])
    print("_____________")




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', '-n', default="", type=str, help="指定名称")
    parser.add_argument('--count', '-c', default=20, type=int, help="查找数量")
    args = parser.parse_args()

    data = {
        'cid1': '0',
        'pageIndex': '1',
        'pageSize': '4'
    }

    count = 0
    pageIndex = 1
    items = []
    while count < args.count:
        data['pageIndex'] = str(pageIndex)
        pageIndex += 1
        response = requests.post('https://try.jd.com/report-details/tryReportPaging.action', headers=headers, data=data)
        resp = response.json()
        if len(resp['list']) == 0:
            break
        for item in resp['list']:
            if args.name in item['skuName']:
                items.append(item)
                count += 1
                print_report(item)



