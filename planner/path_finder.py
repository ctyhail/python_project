import heapq
from collections import defaultdict

class TrainGraph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_train(self, from_station, to_station, depart_time, arrive_time, train_no):
        self.graph[from_station].append({
            'to': to_station,
            'depart': depart_time,
            'arrive': arrive_time,
            'train_no': train_no
        })

    def build_from_12306(self, train_data):
        for item in train_data:
            #parts = item.split('|')
            #if len(parts) < 15:
            #    continue
            train_no = parts[3]
            from_station_code = item['from_station_code']
            to_station_code = item['end_station_code']
            depart_time = parts[8]  # 格式: HH:MM
            arrive_time = item['arrive_time']  # 格式: HH:MM

            try:
                d_h, d_m = map(int, depart_time.split(':'))
                a_h, a_m = map(int, arrive_time.split(':'))
                d_min = d_h * 60 + d_m
                a_min = a_h * 60 + a_m
                if a_min < d_min:
                    a_min += 24 * 60  # 跨天
                self.add_train(from_station_code, to_station_code, d_min, a_min, train_no)
            except:
                continue

    def dijkstra(self, start, end):
        pq = [(0, start, 0, [])]
        visited = dict()

        while pq:
            total_time, curr, arrive_time, path = heapq.heappop(pq)
            if curr in visited and visited[curr] <= total_time:
                continue
            visited[curr] = total_time

            if curr == end:
                return path

            for edge in self.graph[curr]:
                wait = max(edge['depart'] - arrive_time, 0)
                next_time = total_time + wait + (edge['arrive'] - edge['depart'])
                heapq.heappush(pq, (
                    next_time, edge['to'], edge['arrive'],
                    path + [(curr, edge['to'], edge['train_no'], edge['depart'], edge['arrive'])]
                ))
        return None