import numpy

from gensim.models import Word2Vec

named_ents = []
with open('file', 'r') as f:
	for word in f.readlines():
		named_ents.append(word.strip())

true_positives = []
false_positives = []

with open('true_positives', 'r') as f:
	for word in f.readlines():
		true_positives.append(word.strip())

with open('false_positives', 'r') as f:
	for word in f.readlines():
		false_positives.append(word.strip())

print named_ents
print true_positives
print false_positives

model = Word2Vec.load("model3.dat")

TRUES = []
FALSES = []

for word in true_positives:
	try:
		TRUES.append(model[word])
	except:
		pass

for word in false_positives:
	try:
		FALSES.append(model[word])
	except:
		pass


print TRUES
print FALSES
print len(TRUES), len(FALSES)

for word1 in named_ents:
	min_true = 10000000000000
	min_false = 10000000000000
	WORD1 = word1
	try:
		word1 = model[word1]
		for word2 in TRUES:
			dist = numpy.linalg.norm(word1 - word2)
			min_true = min(min_true, dist)
		for word2 in FALSES:
			dist = numpy.linalg.norm(word1 - word2)
			min_false = min(min_false, dist)
#		print WORD1, min_true, min_false
		if min_true < min_false:
			print WORD1
	except Exception as e:
		pass
