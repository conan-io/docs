import bottle
import requests

from bottle import request, response


# the decorator
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if bottle.request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors


app = bottle.app()


@app.route('/search', method=['OPTIONS', 'GET'])
@enable_cors
def search():
    params = request.query.decode()
    version = params.get("version", None)
    keywords = params.get("query", None)

    body = {
        "from": 0, "size": 5,
        "query": {
            "bool": {
                "filter": [
                    {"match": {"version": version}}
                ],
                "should": [
                    {"match": {
                        "html": {
                            "query": keywords,
                            "boost": 1
                        }
                    }},
                    {"match": {
                        "title": {
                            "query": keywords,
                            "boost": 3
                        }
                    }}
                ]
            }
        }
    }
    print(body)
    tmp = requests.get("http://localhost:9200/docs/_search", json=body)
    data = tmp.json()
    response.headers['Content-type'] = 'application/json'
    print(data["hits"]["hits"])
    return data["hits"]


if __name__ == "__main__":
    app.run(port=8001)