from optparse import OptionParser
from collections import Counter

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option('-n', '--n-gram', type='int', dest='ngrams', default=1)
	parser.add_option('-f', '--file', dest='filename', default=1)
	(options, args) = parser.parse_args()

def getCorpus():
	f = open(options.filename, 'r')
	return f

def analyze(corpus):
	frequency_map = Counter()
	word_map = {}
	queue = []
	for line in corpus:
		words = queue + line.split()
		queue = []
		while (len(words) > options.ngrams):
			key = []
			for i in range(options.ngrams):
				key.append(words[i])
			k = tuple(key)
			frequency_map[k] += 1
			if k not in word_map:
				word_map[k] = Counter({words[i + 1]:1})
			else:
				word_map[k].update({words[i + 1]: 1})
			words.pop(0)
		[queue.append(word) for word in words]
	return frequency_map, word_map

def normalize(word_map):
	for key in word_map:
		total = sum(word_map[key].values())
		for k in word_map[key]:
			word_map[key][k] = word_map[key][k] / float(total)
	return word_map

def generate(frequency_map, word_map):
	seed = frequency_map
	return

corpus = getCorpus()
frequency_map, word_map = analyze(corpus)
normalize(word_map)
generate(frequency_map, word_map)