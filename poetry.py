from optparse import OptionParser
from collections import Counter
import util, math, random

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option('-n', '--n-gram', type='int', dest='ngrams', default=1)
	parser.add_option('-f', '--file', dest='filename', default=1)
	parser.add_option('-o', '--output', type='int', dest='npoems', default=1)
	(options, args) = parser.parse_args()
#	npoems = 1

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


def generate2(frequency_map, word_map):
	parameters = [(8,[]) for _ in range(8)]
	poem = util.Poetry(parameters)
	grammar = util.grammar(frequency_map, word_map)

	while not poem:
		curr = poem.getLine()
		while curr:
			word = grammar.next()
			if not word:
				break
			curr.add(word)
		poem.iterate()

	print poem.format()



def generate(frequency_map, word_map):
	output = ""
	seed = ""
	seed_key = util.weightedRandomChoice(frequency_map)
	count = 0
	for i in range(len(seed_key)):
		seed += seed_key[i] + " "
		count += 1
	output += seed

	for _ in range(120 - options.ngrams):
		if seed_key not in word_map:
			break
		next = util.weightedRandomChoice(word_map[seed_key])
		count += 1
		output += next + ("\n" if (count % 8 == 0) else " ")
		broken_seed = seed.split()
		broken_seed.pop(0)
		broken_seed.append(next)
		seed = ' '.join(broken_seed)
		seed_key = tuple(broken_seed)
	return output

def beautify(output, i):
	print "Poem Number:", i
	print output
	print "------------------"
	print ""

corpus = getCorpus()
frequency_map, word_map = analyze(corpus)
#normalize(word_map)

for i in range(options.npoems):
	output = generate2(frequency_map, word_map)
	beautify(output, i)
