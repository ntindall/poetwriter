from optparse import OptionParser
from collections import Counter
import util, math, random
from poetry import * 
from grammar import *

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-n', '--n-gram', type='int', dest='ngrams', default=1)
    parser.add_option('-f', '--file', dest='filename', default=1)
    parser.add_option('-o', '--output', type='int', dest='npoems', default=3)
    (options, args) = parser.parse_args()

#Opens corpus file and collects data about it
#Right now, just does n gram analysis
class Corpus(object):
    def __init__(self, name):
        self.file = open(name, 'r')
        self.frequency_map = Counter()
        self.word_map = {}
    def analyze(self, n):
        queue = []
        for line in self.file:
            words = queue + line.split()
            queue = []
            while (len(words) > n):
                key = []
                for i in range(n):
                    key.append(words[i])
                k = tuple(key)
                self.frequency_map[k] += 1
                if k not in self.word_map:
                    self.word_map[k] = Counter({words[i + 1]:1})
                else:
                    self.word_map[k].update({words[i + 1]: 1})
                words.pop(0)
            [queue.append(word) for word in words]

    def normalize(self):
        for key in self.word_map:
            total = sum(self.word_map[key].values())
            for k in self.word_map[key]:
                word_map[key][k] = word_map[key][k] / float(total)
 
# Generate poetry based on a corpus       
def generate(corpus):
    parameters = [(8,[]) for _ in range(8)]
    poem = Poetry(parameters)
    grammar = Grammar(corpus.frequency_map, corpus.word_map)

    while not poem:
        curr = poem.getLine()
        while curr:
            word = grammar.next()
            if not word:
                break
            curr.add(word)
        poem.iterate()
    return poem.format()

#MAIN EXECUTION
corpus = Corpus(options.filename)
corpus.analyze(options.ngrams)

for i in range(options.npoems):
    output = generate(corpus)
    print output
