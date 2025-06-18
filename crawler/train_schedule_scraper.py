import requests
import json
from datetime import datetime

def query_train_schedule(from_station, to_station, date, top_k, middle_station=''):
    """
    from_station::起始站编号
    to_station::重点站编号
    middle_station::中转站编号
    date::日期

    return::含有满足所有条件的车次信息的列表
    """

    urls = [f"https://kyfw.12306.cn/lcquery/queryU?train_date={date}&from_station_telecode={from_station}&to_station_telecode={to_station}&middle_station={middle_station}&result_index={i*10}&can_query=Y&isShowWZ=N&purpose_codes=00&channel=E" for i in range(top_k//10+1)]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    }

    trains = []
    for url in urls:
        try:
            response = requests.get(url, headers=headers)
        except:
            break
        #print(response.text)
        try:
            train = response.json()['data']['middleList']
            trains.extend(train)
        except:
            print("获取失败，可能是反爬限制。")
    
    return trains
    

if __name__ == '__main__':
    # 示例使用：北京 -> 天津
    from_station = 'BJP'
    to_station = 'TJP'
    date = datetime.today().strftime('%Y-%m-%d')
    query_train_schedule(from_station, to_station, date)
