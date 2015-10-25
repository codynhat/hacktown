from elasticsearch import Elasticsearch
from random import randint


def randomBadLocations():
	es = Elasticsearch(['http://107.170.211.113:9200'])
	size = 100
	res = es.search(index="index", body={"query": {"match_all": {}}}, doc_type="bad", size=size)["hits"]["hits"]
	result = []
	for r in res:
		a = {"loc": r["_source"]["location"]}
		loc = a["loc"]
		if (loc != ''):
			result.append(loc)
	index = randint(0, size - 6)
	print index
	print {result[index], result[index+1], result[index+2], result[index+3], result[index+4]}


if __name__ == "__main__":
    randomBadLocations()