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
	output = ""
	seed = ""
	seed_key = frequency_map.most_common(1)[0][0]
	for i in range(len(frequency_map.most_common(1)[0][0])): #hacky shit
		seed += frequency_map.most_common(1)[0][0][i] + " "
	output += seed

	for _ in range(100):
		next = word_map[seed_key].most_common(1)[0][0]
		output += next + " "	
		broken_seed = seed.split()
		print broken_seed
		broken_seed.pop(0)
		broken_seed.append(next)
		seed = ' '.join(broken_seed)
		seed_key = tuple(broken_seed)
		print seed_key
	print output

corpus = getCorpus()
frequency_map, word_map = analyze(corpus)
normalize(word_map)
generate(frequency_map, word_map)