from nltk.corpus import stopwords
from elasticsearch import Elasticsearch
import frequency

def deleteCommonWords(badLocationData):

	theStopwordsDic = set(stopwords.words('english'))
	locations = []

	for line in badLocationData:
		print line
		a = filter(lambda word: not word in theStopwordsDic,line)
		if (a != ""):
			locations.append(a)
	return locations


def main():
	es = Elasticsearch(['http://107.170.211.113:9200'])
	res = es.search(index="index", body={"query": {"match_all": {}}}, doc_type="bad", size=20)["hits"]["hits"]
	result = []
	for r in res:
		a = {"loc": r["_source"]["location"]}
		loc = a["loc"]
		result.append(loc)
	s = deleteCommonWords(result)
	frequency.doTheTuples(s)

if __name__ == "__main__":
    main()