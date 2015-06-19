#!/usr/bin/python

from flask import Flask, render_template
app = Flask(__name__)

import json
from pyelasticsearch import ElasticSearch


@app.route("/")
@app.route("/index")
def hello():
    return "Hello World"

@app.route("/es_test/<lat>/<lon>/")
def es_test(lat, lon):
    ELASTIC_SEARCH_CLUSTER = [
    "http://52.8.145.247:9200/", "http://52.8.148.251:9200/", "http://52.8.158.130:9200/", "http://52.8.162.105:9200/",
    "http://52.8.153.92:9200/"]

    es_client = ElasticSearch(urls=ELASTIC_SEARCH_CLUSTER)

    location = {
        "lat": lat,
        "lon": lon
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

    coords = []
    print type(hits)
    for ob in hits:
        source = ob['_source']
        lat = source['location']['lat']
        lon = source['location']['lon']
        coords.append((lat, lon))

        # Render the page;
    return render_template("output.html",
            best_lon = lon,
            best_lat = lat,
            coords = json.dumps(list(coords))
            )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)