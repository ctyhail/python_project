from planner.path_finder import TrainGraph
from crawler.train_schedule_scraper import query_train_schedule
from crawler.station_parser import fetch_station_codes
from crawler.train_price_scraper import query_train_price
import json
from datetime import datetime
import os

def load_station_mapping():
    with open('data/stations.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def simulate_live_query():
    stations = load_station_mapping()
    reverse_map = {v: k for k, v in stations.items()}
    
    from_city = str(input("起始地："))
    to_city = str(input("目的地："))
    date = str(input("日期（年-月-日）："))
    #date = datetime.today().strftime('%Y-%m-%d')

    from_code = stations.get(from_city)
    to_code = stations.get(to_city)

    if not from_code or not to_code:
        print("城市名未找到")
        return

    train_data = query_train_schedule(from_code, to_code, date)
    if not train_data:
        print("未获取到车次数据")
        return

    """
    graph = TrainGraph()
    graph.build_from_12306(train_data)
    result = graph.dijkstra(from_code, to_code)
    if result:
        print("\n最优路径如下：")
        for step in result:
            dep_h, dep_m = divmod(step[3], 60)
            arr_h, arr_m = divmod(step[4], 60)
            print(f"{reverse_map.get(step[0], step[0])} -> {reverse_map.get(step[1], step[1])} | 车次: {step[2]} | {dep_h:02d}:{dep_m:02d} - {arr_h:02d}:{arr_m:02d}")
    else:
        print("未找到路径")

    """
    for i, item in enumerate(train_data):
        try:
            price = 0.0
            all_time = item['all_lishi']
            arrive_date = item['arrive_date']
            arrive_time = item['arrive_time']
            middleStations = []
            from_station_name = item['from_station_name']
            end_station_name = item['end_station_name']
            for middleTrain in item['fullList']:
                train_no = middleTrain['train_no']
                s_code = middleTrain['from_station_telecode']
                e_code = middleTrain['to_station_telecode']
                middleTrainDate = middleTrain['start_train_date'][:4] + '-' + middleTrain['start_train_date'][4:6] + '-' + middleTrain['start_train_date'][6:]

                #拟编写选择票价方案
                middleTrainPrice = query_train_price(s_code,e_code,middleTrainDate,train_no)
                #print(min([int(value)] for value in middleTrainPrice.values()))
                price += min([int(value)] for value in middleTrainPrice.values())[0] / 10

                if middleTrain['to_station_name'] == to_city or to_city in middleTrain['to_station_name']:
                    break
                middleStations.append(middleTrain['to_station_name'])
            print(f"{i+1}号方案：{from_station_name}->", end='')
            for middleStation in middleStations:
                print(f"{middleStation}->",end='')
            print(f"{end_station_name}")
            print(f"\t乘车时间:{all_time} 抵达目的地时间为{arrive_date} {arrive_time} 总票价:{price}")
        except:
            pass
    

    
if __name__ == '__main__':
    if not os.path.exists('data/stations.json'):
        fetch_station_codes()
    simulate_live_query()
