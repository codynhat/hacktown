"""
Very simple Flask web site, with one page
displaying a course schedule.

"""

import flask
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify  # For AJAX transactions

import json
import logging
from elasticsearch import Elasticsearch
from random import randint


###
# Globals
###
app = flask.Flask(__name__)
import CONFIG

import uuid
app.secret_key = str(uuid.uuid4())
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)

es = Elasticsearch(['http://localhost:9200'])

###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
  app.logger.debug("Main page entry")

  return flask.render_template('index.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] =  flask.url_for("index")
    return flask.render_template('page_not_found.html'), 404

#################
#
# Functions used within the templates
#
#################

@app.route("/_tweet_calcs")
def calc_tweets():
    query = request.args['query']
    query = query.lower()
    result = []
    c = 0
    while c < 10000:
        res = es.search(index="index", body={"query": {"match_all": {}}}, doc_type=query, size=1000, from_=c)["hits"]["hits"]
        for r in res:
            a = {"lat": r["_source"]["lat"], "lng": r["_source"]["lng"], "wgt": r["_source"]["score"], "name": r["_source"]["name"], "text": r["_source"]["text"]}
            result.append(a)
            c += 1000
    return jsonify({"result": result})

@app.route("/munging")
def munging():
    size = 100
    res = es.search(index="index", body={"query": {"match_all": {}}}, doc_type="bad", size=size)["hits"]["hits"]
    query = []
    for r in res:
        a = {"loc": r["_source"]["location"]}
        loc = a["loc"]
        if loc:
            query.append(loc)
    index = randint(0, size - 6)
    result = []
    result = query[index:index+5];
    return jsonify({"result": result})

#############


if __name__ == "__main__":
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT)
