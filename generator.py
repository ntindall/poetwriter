#STD LIBRARIES
from optparse import OptionParser
import util, math, random

#CUSTOM LIBRARIES
import en #NLP library
from wordnik import * #dictionary with part of speech, synonyms, related word
apiUrl = 'http://api.wordnik.com/v4'
apiKey = '1453b0da46be3985ab0040b354601405dbb094b3e77e51454'
client = swagger.ApiClient(apiKey, apiUrl)

#FILES
from poetry import * 
from grammar import *

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-n', '--n-gram', type='int', dest='ngrams', default=1)
    parser.add_option('-f', '--file', dest='filename', default=1)
    parser.add_option('-o', '--output', type='int', dest='npoems', default=3)
    (options, args) = parser.parse_args()
 
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

for i in range(options.npoems):
    output = generate(corpus)
    print output
# END