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

# Opens corpus file and collects data about it
# Right now, just does n gram analysis
class Corpus(object):
    def __init__(self, name):
        self.file = open(name, 'r')
        self.frequency_map = Counter()
        self.word_map = {}
    
    # n-gram algorithm, looks backward
    # Makes a dictionary with keys of len (n) and values of len 1.
    # Perhaps a better implementation for our purposes does forward
    # looking? I.e. keys of len(1) and values of len(n). This would
    # lead to a richer dictionary output. Can select value[0] to be
    # next word as defined by the grammar. 
    def analyze(self, n):
        queue = []
        for line in self.file:
            words = queue + line.split() # current words to be considered
            queue = [] # reset queue upon reading new line
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
            [queue.append(word) for word in words] #add leftover words to queue

    def normalize(self):
        for key in self.word_map:
            total = sum(self.word_map[key].values())
            for k in self.word_map[key]:
                word_map[key][k] = word_map[key][k] / float(total)
 
# Generate poetry based on a corpus       
def generate(corpus):
    parameters = [(8,[]) for _ in range(8)] #stub, assumed 8 syllables (words) per line
    poem = Poetry(parameters)
    grammar = Grammar(corpus.frequency_map, corpus.word_map)

    while not poem:
        curr = poem.getLine()
        while curr:
            word = grammar.next()
            if not word: # Seed has no successsor words
                break
            if not curr.add(word):
                # Word doesn't fit, try a different one
                # Will get stuck here under a rigid syllable counting system
                # Need to add flexibility within grammar to prevent failure
                # See util.getSyllables
                continue
            grammar.update(word) #word added successfully, update seed
        poem.iterate()
    return poem.format()

#########################################################################
# MAIN EXECUTION
#########################################################################

corpus = Corpus(options.filename)
corpus.analyze(options.ngrams)
#print corpus.frequency_map

for i in range(options.npoems):
    output = generate(corpus)
    print output
# END