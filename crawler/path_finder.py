import heapq
from collections import defaultdict

class TrainGraph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_train(self, from_station, to_station, depart_time, arrive_time, train_no):
        # depart_time 和 arrive_time 为分钟制
        self.graph[from_station].append({
            'to': to_station,
            'depart': depart_time,
            'arrive': arrive_time,
            'train_no': train_no
        })

    def dijkstra(self, start, end):
        # 优先队列: (当前总耗时, 当前站点, 到达时间, 路径记录)
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
