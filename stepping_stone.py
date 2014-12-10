# FILE: stepping_stone.py
# ---------------------------------
# Stepping stone for generator.py implementation
# ARCHAIC FILE. DOES NOT FUNCTION.

#STD LIBRARIES
from optparse import OptionParser
import math, random, copy, operator, time, numpy

#FILES
import searchutil, util
from poetry import * 
from grammar import *

if __name__ == '__main__':
    parser = OptionParser()

    # Order of the n gram model
    parser.add_option('-n', '--n-gram', type='int', dest='ngrams', default=1)

    # Corpus file, used to train the languaeg model
    parser.add_option('-f', '--file', dest='filename', default=1)

    # The number of poems to be output
    parser.add_option('-o', '--output', type='int', dest='npoems', default=3)

    # The phrase length (number of lines that the n-gram wraps around before reseeding)
    parser.add_option('-l', '--sentence-length', type='int', dest='sentenceLength', default=1)

    # The type of corpus, in order to facilitate corpus cleanup
    parser.add_option('-s', '--source', dest='source')

    # Whether the model is probabalistic when selecting actions (if not selected, chooses 
    # more frequent seeds first. 
    parser.add_option('-p', '--probabilistic', type='int', dest='probabilistic', default=1)

    # The number of initial seeds to try before backtracking (when the grammar is reseeded)
    parser.add_option('-b', '--begin-seeds', type='int', dest='beginseeds', default=5)

    # The number of children seeds to try before backtracking, selects the b most frequent 
    # children or the first b children seeded (if probabilistic)
    parser.add_option('-r', '--branching', type='int', dest='branching')

    # The type of poetry to output (options: sonnet, haiku, eight, octave)
    parser.add_option('-t', '--type', dest='type', default='sonnet')

    # Verbosity of the generator module
    parser.add_option('-v', '--verbose', type='int', dest='verbose', default=0)
    (options, args) = parser.parse_args()

# Generate poetry based on a corpus, stepping stone implementation     
def generate(corpus):
    parameters = [(8,[]) for _ in range(2)] #stub, assumed 8 syllables (words) per line
    poem = Poetry(parameters, options.sentenceLength)
    grammar = Grammar(corpus.frequency_map, corpus.word_map, corpus.begin_map)

    while not poem:
        print poem
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
    return poem

############# MAIN EXECUTION

corpus = Corpus(options.filename)
corpus.analyze(options.ngrams, options.source)
if (options.verbose > 2):
    print corpus.word_map

# Part of stepping stone
for i in range(options.npoems):
    print generate(corpus)
# END
