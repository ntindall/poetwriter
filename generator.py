#STD LIBRARIES
from optparse import OptionParser
import math, random, copy, operator

#CUSTOM LIBRARIES
import en #NLP library
from wordnik import * #dictionary with part of speech, synonyms, related word
apiUrl = 'http://api.wordnik.com/v4'
apiKey = '1453b0da46be3985ab0040b354601405dbb094b3e77e51454'
client = swagger.ApiClient(apiKey, apiUrl)

#FILES
import searchutil, util
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

class PoetrySearchProblem(searchutil.SearchProblem):

    def __init__(self, poem, grammar): 
        self.poem, self.grammar = poem, grammar

    # Poem object passed into problem, with syllabic and rhyme
    # constraints initialized with the object
    def startState(self):
        #(current poem state, seed)
        return self.poem, None

    # Goal has been reached when the poem is completed.
    # Poetry objects keep track of their current progress, and will
    # evaluate true once they are completed. 
    def isGoal(self, state):
        poem, seed = state
        return poem

    # Return a list of (action, newState, cost) tuples corresponding to edges
    # coming out of |state|.
    def succAndCost(self, state):
        #(current poem state, seed)
        poem, seed = state

        # Initial call, seed needs to be initialized. 
        # -------------------------------------------
        if not seed:
            #Assumption: the initial seed will fit on the first line. 

            seed = util.weightedRandomChoice(self.grammar.frequency_map)
            new_poem = copy.deepcopy(poem) #necessary
            words = ""
            for i in range(len(seed)): #push seeds into first line
                new_poem.getLine().add(seed[i])
            self.poem = new_poem
            return [(seed, (new_poem, seed), 0)]
        
        # Branching calls
        # -------------------------------------------
        result = []
        print poem #comment out if you want to see the poem being constructed

        # IMPORTANT NOTE
        # For every successor word, consider all possible children nodes.
        # Pruning to meet rhyming and syllabic constraints of actions needs to be
        # performed here. There is no error checking in the Line or Poetry objects.
        # The rhyming word needs to be passed back and forth between Poetry and Line
        # objects once they are completed (not implemented)
        if seed in self.grammar.word_map: 
            for word, frequency in self.grammar.word_map[seed].iteritems(): #CONSIDER ALL POSSIBLE BRANCHES
            # word: the word that follows the current seed given the n-gram model
            # frequency: the number of times that that word occurs after the given seed
                new_poem = copy.deepcopy(poem) #necessary
                curr = new_poem.getLine()
                if curr: 
                    if curr.add(word): #if the word fits on the current line
                        broken_seed = [seed[i] for i in range(len(seed))]
                        broken_seed.pop(0)
                        broken_seed.append(word)
                        new_seed = tuple(broken_seed)
                        cost = frequency
                        if not curr: #line has been finished
                            if curr.propagator:
                                for line_i in curr.paired_indices:
                                    if new_poem[line_i].constraint == "": #line has no previous constraint
                                        new_poem[line_i].constraint = word
                            new_poem.iterate()
                        result.append((word, (new_poem, new_seed), cost))
            # Idea: sort by descending frequencies so that it looks down more likely paths first
            result.sort(key=operator.itemgetter(2), reverse=True)
        return result

#########################################################################
# MAIN EXECUTION
#########################################################################

# Example usage:
# python generator.py -n 2 -f "lyrics/eminem.txt" -o 4

corpus = Corpus(options.filename)
corpus.analyze(options.ngrams)
#print corpus.word_map

# NEW
# About the pairs.
# Assumption, pairs are increasing (propagator, receiver) 
# order, can't propagate to self. Chains must be fully realized,
# i.e. [(0,1), (0,7), (6,7)] is invalid, while [(0,1), (0,6),(0,7),(6,7)]
# is valid (though the last item is redundant).
# [(0,1),(0,5),(2,3),(3,4),(5,6),(6,7)] will work, while [(0,1),(0,7),(2,3),(3,4),(5,6),(6,7)]
# will yield errors, better to be consistent: [(0,1), (0,5), (0,6),(0,7),(2,3),(2,4)]
# Successive chains are safe, while separated ones require more tentative handling



# pairs = [(0,2),(1,3),(4,6),(5,7),(8,10),(9,11),(12,13)]
# haiku = [(5,[]),(7,[]),(5,[])]
# parameters = [(10, pairs) for _ in range(14)] #stub, assumed 8 syllables (words) per line
pairs = [(0,1),(2,3),(4,5),(6,7)]
parameters = [(10, pairs) for _ in range(8)] #stub, assumed 8 syllables (words) per line
grammar = Grammar(corpus.frequency_map, corpus.word_map)

for i in range(options.npoems):
    poem = Poetry(parameters)
    problem = PoetrySearchProblem(poem, grammar)

    #UNIFORM COST SEARCH (DJIKSTRA'S)
    #ucs = searchutil.UniformCostSearch(verbose=1)
    #ucs.solve(problem)
    #solution, final_seed = ucs.solution

    #DEPTH FIRST SEARCH
    bts = searchutil.DepthFirstSearch(verbose=1)
    bts.solve(problem)
    print ""
    if bts.solution:
        solution, final_seed = bts.solution
        print "RESULT"

        print solution
    else:
        print "NO SOLUTION FOUND"
#NEW


# for i in range(options.npoems):
#     output = generate(corpus)
#     print output
# END
