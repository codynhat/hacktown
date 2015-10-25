from elasticsearch import Elasticsearch
es = Elasticsearch()
es.indices.create(index='index', ignore=400)