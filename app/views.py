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


@app.route('/map/<user_lat>/<user_lon>')
def realtime(user_lat, user_lon):
    ELASTIC_SEARCH_CLUSTER = [
        "http://52.8.209.213:9200/",
        "http://52.8.209.72:9200/",
        "http://52.8.185.120:9200/",
        "http://52.8.55.191:9200/",
        "http://52.8.153.92:9200/"]

    es_client = pyelasticsearch.ElasticSearch(urls=ELASTIC_SEARCH_CLUSTER)

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
        "filter": {
            "geo_distance": {
                "distance": "2km",
                "location": location
            }
        }
    }

    print "executing search query"
    res = es_client.search(query, index="taxi_index")
    hits = res['hits']['hits']
    hits_len = len(hits)

    print "found %s hits" % hits_len
    # print json.dumps(hits)

    cabs = []

    for ob in hits:
        taxi_id = ob['_id']
        source = ob['_source']
        lat = source['location']['lat']
        lon = source['location']['lon']
        cabs.append({'name': taxi_id, 'lat': lat, 'lng': lon})

    print json.dumps(cabs)

    return jsonify(cabs=cabs)
