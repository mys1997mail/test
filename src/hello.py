from flask import Flask, request, jsonify
import redis
app = Flask(__name__)

cache = redis.Redis(host = "redis")

def fibonacci(n):
    a, b, res = 1, 1, 1
    if n <= 1:
        return n
    else:
        for i in range(2, n):
            res = a + b
            a = b
            b = res
    return res

@app.route('/fib')
def hello():
    from_index = request.args.get('from')
    from_index = int(from_index) if from_index and from_index.isdigit() else None
    to_index = request.args.get('to')
    to_index = int(to_index) if to_index and to_index.isdigit() else None
    if not from_index and not to_index:
        raise Exception(f"Wrong params in request. Should be contain one of (from, to) at least")
    if not from_index:
        from_index = 1
    if not to_index:
        to_index = from_index
    result = []
    for i in range(from_index, to_index + 1):
        cachedValue = cache.get(i)
        if cachedValue:
            app.logger.debug(f"Get from cache by {i} - {cachedValue}")
            result.append(int(cachedValue))
        else:
            app.logger.debug(f"No cached Value. Calculate {i} fib")
            temp = fibonacci(i)
            cache.set(i, temp)
            result.append(temp)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')