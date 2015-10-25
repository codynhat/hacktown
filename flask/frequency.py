import collections

def doTheTuples(arrayOfStrings):
	a = arrayOfStrings
	counter = collections.Counter(a)
	topFive = counter.most_common(5)
	topBadTopics = [x[0] for x in topFive]
	return topBadTopics