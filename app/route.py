import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from crawler.train_schedule_scraper import query_train_schedule
from crawler.station_parser import fetch_station_codes
from crawler.train_price_scraper import query_train_price
import json
from datetime import datetime
import os

def load_station_mapping():
    with open('data/stations.json', 'r', encoding='utf-8') as f:
        return json.load(f)
    
def time_to_minutes(time_str):
    """将 'hh:mm' 转为分钟"""
    h, m = map(int, time_str.split(":"))
    return h * 60 + m

def parse_duration(duration_str):
    """将 'hh:mm' 转为总分钟数"""
    if ':' in duration_str:
        h, m = map(int, duration_str.split(":"))
        return h * 60 + m
    return 0

def search_transfer_routes(from_city, to_city, date, start_time, end_time, strategy, top_k=5, middle_station=''):
    # 使用 stations.json，query_train_schedule，query_train_price
    # 返回结果为 JSON 格式的中转方案列表
    # 与 simulate_live_query 相同逻辑，只是不 print，返回列表
    
    stations = load_station_mapping()
    #reverse_map = {v: k for k, v in stations.items()}
    

    from_code = stations.get(from_city)
    to_code = stations.get(to_city)
    if middle_station != '':
        mid_code = stations.get(middle_station)
    else:
        mid_code = ''

    if not from_code or not to_code:
        print("城市名未找到")
        return

    train_data = query_train_schedule(from_code, to_code, date, top_k=top_k, middle_station=mid_code)
    if not train_data:
        print("未获取到车次数据")
        return

    routes = []
    time_window_start = time_to_minutes(start_time)
    time_window_end = time_to_minutes(end_time)

    for item in train_data:
        try:
            all_time = item['all_lishi_minutes']
            wait_time = item['wait_time_minutes']
            arrive_date = item['arrive_date']
            arrive_time = item['arrive_time']
            from_station_name = item['from_station_name']
            end_station_name = item['end_station_name']
            full_list = item['fullList']

            first_departure = full_list[0]['start_time']
            depart_minute = time_to_minutes(first_departure)
            if not (time_window_start <= depart_minute <= time_window_end):
                continue

            total_price = 0.0
            total_time = all_time
            route_stations = []
            train_ids = []

            for middleTrain in full_list:
                train_no = middleTrain['train_no']
                s_code = middleTrain['from_station_telecode']
                e_code = middleTrain['to_station_telecode']
                middleTrainDate = middleTrain['start_train_date'][:4] + '-' + middleTrain['start_train_date'][4:6] + '-' + middleTrain['start_train_date'][6:]

                price_dict = query_train_price(s_code, e_code, middleTrainDate, train_no)
                if not price_dict:
                    raise ValueError("票价获取失败")
                price_min = min([int(v) for v in price_dict.values()])
                total_price += price_min / 10

                train_ids.append(train_no)
                #防止终点站出现两次
                if middleTrain['to_station_name'] == to_city or to_city in middleTrain['to_station_name']:
                    break
                route_stations.append(middleTrain['to_station_name'])

            routes.append({
                "from": from_station_name,
                "to": end_station_name,
                "arrive_date": arrive_date,
                "arrive_time": arrive_time,
                "route": route_stations,
                "trains": train_ids,
                "total_price": total_price,
                "total_time": total_time,
                "depart_time": first_departure,
                "wait_time": wait_time
            })

        except Exception as e:
            print("⚠️ 跳过异常方案：", e)
            continue

    if not routes:
        print("没有符合条件的方案")
        return

    # 排序所有方案
    if strategy == 'cheapest':
        routes.sort(key=lambda x: x['total_price'])
    elif strategy == 'fastest':
        routes.sort(key=lambda x: x['total_time'])
    else:
        print("策略错误，应为 'cheapest' 或 'fastest'")
        return

    #print(routes)
    return routes[:top_k]  # 示例最多返回 10 条



if __name__ == "__main__":
    from_city = '重庆'
    to_city = '桂林'
    date = '2025-06-18'
    start_time = '06:00'
    end_time = '22:00'
    strategy = 'cheapest'
    top_k = 5
    print(search_transfer_routes(from_city, to_city, date, start_time, end_time, strategy, top_k, middle_station=''))