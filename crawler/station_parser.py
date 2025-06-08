import requests
import re
import json

def fetch_station_codes():
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    raw_text = response.text

    raw_data = raw_text.split('=')[1].strip(" ';\n")
    items = raw_data.split('@')[1:]  # 第一个是空的
    stations = {}

    for item in items:
        parts = item.split('|')
        if len(parts) >= 3:
            name = parts[1]  # 中文站名
            code = parts[2]  # 简码
            stations[name] = code


    # 保存到本地文件
    with open(r'G:\py_project\12306\station\data\stations.json', 'w', encoding='utf-8') as f:
        json.dump(stations, f, ensure_ascii=False, indent=2)
    print(f"共获取 {len(stations)} 个站点。")

if __name__ == '__main__':
    fetch_station_codes()