from elasticsearch import Elasticsearch
es = Elasticsearch(['http://107.170.211.113:9200'])
es.indices.create(index='index', ignore=400)