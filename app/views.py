__author__ = 'myho'

# Create views for the html page
import json

from flask import jsonify, render_template
import pyelasticsearch

from app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/realtime/<user_lat>/<user_lon>')
def realtime(user_lat, user_lon):
    ELASTIC_SEARCH_CLUSTER = [
        "http://52.8.145.247:9200/", "http://52.8.148.251:9200/", "http://52.8.158.130:9200/",
        "http://52.8.162.105:9200/",
        "http://52.8.153.92:9200/"]

    es_client = pyelasticsearch.ElasticSearch(urls=ELASTIC_SEARCH_CLUSTER)

    # hard-code for testing
    # user_lat = 37.7577
    # user_lon = -122.4376
    location = {
        "lat": user_lat,
        "lon": user_lon
    }

    # construct query to find closest taxi
    query = {
        "from": 0,
        "size": 10,
        "query": {
            "match": {
                "is_occupied": "0"
            }
        },
        "sort": [
            {
                "_geo_distance": {
                    "location": location,
                    "order": "asc",
                    "unit": "km"
                }
            }
        ]
    }

    print "executing search query"
    res = es_client.search(query, index="taxi_index")
    hits = res['hits']['hits']
    hits_len = len(hits)

    print json.dumps(hits)

    print type(hits)

    cabs = []

    for ob in hits:
        taxi_id = ob['_id']
        source = ob['_source']
        lat = source['location']['lat']
        lon = source['location']['lon']
        cabs.append({'name': taxi_id, 'lat': lat, 'lng': lon})

    return jsonify(cabs=cabs)
