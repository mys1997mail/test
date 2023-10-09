from flask import Flask, request, jsonify
import redis
app = Flask(__name__)

cache = redis.Redis(host = "redis")

class InvalidUsage(Exception):
    status_code = 422

    def __init__(self, message, status_code = None, payload = None):
        Exception.__init__(self)
        self.message = message
        if not status_code:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = {"message": self.message}
        if self.payload:
            rv['payload'] = self.payload
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

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

def get_index_from_request(arg_name):
    index = request.args.get(arg_name)
    return int(index) if index and index.isdigit() else None

@app.route('/fib')
def hello():
    from_index = get_index_from_request('from') or 1
    to_index = get_index_from_request('to') or from_index

    if from_index is None and to_index is None:
        raise InvalidUsage("Wrong params in request. Should contain at least one of (from, to)")
    
    if to_index < from_index:
        raise InvalidUsage("'To' parameter shoulb be greater or equal than 'from' parameter")
    
    result = get_fibonacci_for_range(from_index, to_index)

    return jsonify(result)

def get_fibonacci_for_range(from_index, to_index):
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
    return result

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')