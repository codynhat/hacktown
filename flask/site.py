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

###
# Globals
###
app = flask.Flask(__name__)
import CONFIG

import uuid
app.secret_key = str(uuid.uuid4())
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)

es = Elasticsearch()

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
    res = es.search(index="index", body={"query": {"match_all": {}}}, doc_type=query, size=100)["hits"]["hits"]
    result = []
    for r in res:
        a = {"lat": r["_source"]["lat"], "lng": r["_source"]["lng"], "wgt": r["_source"]["score"]}
        result.append(a)
    return jsonify({"result": result})


#############


if __name__ == "__main__":
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT)
