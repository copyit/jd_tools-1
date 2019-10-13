#coding=utf-8
from urllib import parse
import json

data = 'adid=D20FCC8E-56EA-4FA3-87D0-99D8AF17BCE3&area=1_2901_55554_0&body=%7B%22shopId%22%3A%221000224204%22%2C%22source%22%3A%22app-shop%22%2C%22latWs%22%3A%2240.085869%22%2C%22lngWs%22%3A%22116.368797%22%2C%22displayWidth%22%3A%221053.000000%22%2C%22sourceRpc%22%3A%22shop_app_home_home%22%2C%22lng%22%3A%22116.481916%22%2C%22lat%22%3A%2240.007001%22%2C%22venderId%22%3A%221000224204%22%7D&build=166619&client=apple&clientVersion=8.2.6&d_brand=apple&d_model=iPhone11%2C2&eid=eidIf8c38121b2sfTitpdPT2RYezQi3M1vMzfU4rauG2wf514U0dUhOixz5SVBsO3HkC/VpQZdl5tjmiT%2BXE83JAn33wZS2sc%2BhtiRS%2B51/1hf7za2Zl&isBackground=N&joycious=96&lang=en_US&networkType=wifi&networklibtype=JDNetworkBaseAF&openudid=55d32ef767c118e0963e1e145a9b9dfb247d951a&osVersion=13.1.2&partner=apple&rfs=0&scope=01&screen=1125%2A2436&sign=57b074b5dcd5a5e90bef65e7c068a2be&st=1570878645596&sv=121&uuid=coW0lj7vbXVin6h7ON%2BtMNFQqYBqMahr&wifiBssid=unknown'

# print(parse.urlencode())
data = parse.unquote(data)
x = dict()
for i in data.split('&'):
    x[i.split('=')[0]] = i.split('=')[1]
print(x)
s = parse.urlencode(x)
#print(s)
print(json.dumps(x))