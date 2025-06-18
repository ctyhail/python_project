from flask import Flask, request, jsonify
from flask_cors import CORS
from route import search_transfer_routes

app = Flask(__name__)
CORS(app)

@app.route('/api/search')
def search():
    from_city = request.args.get("from")
    to_city = request.args.get("to")
    date = request.args.get("date")
    start_time = request.args.get("startTime", "06:00")
    end_time = request.args.get("endTime", "22:00")
    strategy = request.args.get("strategy", "cheapest")
    top_k = int(request.args.get("top_k"))
    middle_station = request.args.get("middle_station", "")

    # 查询逻辑（调用你的查询模块）
    routes = search_transfer_routes(from_city, to_city, date, start_time, end_time, strategy, top_k, middle_station)
    
    return jsonify(routes)


if __name__ == '__main__':
    app.run()