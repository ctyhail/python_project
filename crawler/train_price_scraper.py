import requests
import json
from datetime import datetime
import os
import time

def query_train_price(from_station, to_station, date, train_no):

    """
    return 以列表的形式返回该车次的所有票的价格
    """

    #time.delay(100)
    #print(from_station, to_station, date, train_no)

    url = f'https://kyfw.12306.cn/otn/leftTicketPrice/queryAllPublicPrice?leftTicketDTO.train_date={date}&leftTicketDTO.from_station={from_station}&leftTicketDTO.to_station={to_station}&purpose_codes=ADULT'

    header = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
    }

    response = requests.get(url,header)
    #print(response.text)
    response = response.json()['data']

    price = {}

    for item in response:
        if item['queryLeftNewDTO']['train_no'] == train_no:
            for key, value in item['queryLeftNewDTO'].items():
                if 'price' in key:
                    price[key] = value

    #print(price)
    return price


