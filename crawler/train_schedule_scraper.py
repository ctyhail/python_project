import requests
import json
from datetime import datetime

def query_train_schedule(from_station, to_station, date):
    #url = f"https://kyfw.12306.cn/lcquery/queryU?train_date=2025-06-07&from_station_telecode=TJP&to_station_telecode=GIW&middle_station=&result_index=0&can_query=Y&isShowWZ=N&purpose_codes=00&channel=E"
    url = f"https://kyfw.12306.cn/lcquery/queryU?train_date={date}&from_station_telecode={from_station}&to_station_telecode={to_station}&middle_station=&result_index=0&can_query=Y&isShowWZ=N&purpose_codes=00&channel=E"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        #'Cookie': 'RAIL_DEVICEID=xxxx; RAIL_EXPIRATION=xxxx'  # 注意：需要有效 cookie
        #'Cookie' : 'JSESSIONID=9CD9C252EA7B7ABB1952703C0835796D; _jc_save_wfdc_flag=dc; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; _big_fontsize=0; route=6f50b51faa11b987e576cdb301e545c4; BIGipServerotn=1473839370.24610.0000; BIGipServerpassport=971505930.50215.0000; BIGipServerportal=2949906698.17695.0000; _jc_save_fromStation=%u5929%u6D25%2CTJP; _jc_save_toStation=%u8D35%u9633%2CGIW; _jc_save_fromDate=2025-06-07; _jc_save_toDate=2025-06-07'
        #'Cookie' : 'SESSIONID=DEE636AA27337F933D7A41C256B6C5D8; _jc_save_wfdc_flag=dc; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; _big_fontsize=0; route=6f50b51faa11b987e576cdb301e545c4; BIGipServerotn=1473839370.24610.0000; BIGipServerpassport=971505930.50215.0000; BIGipServerportal=2949906698.17695.0000; _jc_save_fromStation=%u5929%u6D25%2CTJP; _jc_save_toStation=%u8D35%u9633%2CGIW; _jc_save_fromDate=2025-06-07; _jc_save_toDate=2025-06-07; uKey=026e49dfb540ad43e1129ffed4c00b0cb2c7eb6b8accc46960890439afc472da'
    }

    
    response = requests.get(url, headers=headers)
    #print(response.text)
    try:
        trains = response.json()['data']['middleList']
        print(trains)
        
        #print(trains)
        print(f"共获取 {len(trains)} 个车次。")
        return trains
    except:
        print("获取失败，可能是反爬限制。")
        return []

if __name__ == '__main__':
    # 示例使用：北京 -> 天津
    from_station = 'BJP'
    to_station = 'TJP'
    date = datetime.today().strftime('%Y-%m-%d')
    query_train_schedule(from_station, to_station, date)
