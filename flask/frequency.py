import collections

def doTheTuples(arrayOfStrings):
	a = arrayOfStrings
	counter = collections.Counter(a)
	print(counter.most_common(5))
