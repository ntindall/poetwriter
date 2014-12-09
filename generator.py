#STD LIBRARIES
from optparse import OptionParser
import math, random, copy, operator, time

#FILES
import searchutil, util
from poetry import * 
from grammar import *

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-n', '--n-gram', type='int', dest='ngrams', default=1)
    parser.add_option('-f', '--file', dest='filename', default=1)
    parser.add_option('-o', '--output', type='int', dest='npoems', default=3)
    parser.add_option('-l', '--sentence-length', type='int', dest='sentenceLength', default=1)
    parser.add_option('-s', '--source', dest='source')
    parser.add_option('-p', '--probabilistic', type='int', dest='probabilistic', default=1)
    parser.add_option('-b', '--begin-seeds', type='int', dest='beginseeds', default=5)
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

    def __init__(self, poem, grammar, ngrams, probabilistic, beginseeds): 
        self.poem, self.grammar, self.ngrams = poem, grammar, ngrams
        self.probabilistic = probabilistic
        self.beginseeds = beginseeds

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
        numSeeds = self.beginseeds
        # Initial call, seed needs to be initialized. 
        # -------------------------------------------
        if not seed:
            toReturn = []
            #Assumption: the initial seed will fit on the first line.
            for _ in range(numSeeds):
                seed = util.weightedRandomChoice(self.grammar.frequency_map)
                while ((seed[0] not in self.grammar.begin_map) or ('-BEGIN-' in seed)):
                    seed = util.weightedRandomChoice(self.grammar.frequency_map)
                new_poem = copy.deepcopy(poem) #necessary
                for i in range(len(seed)): #push seeds into first line
                    new_poem.getLine().add(seed[i])
                self.poem = new_poem
                toReturn.append([(seed, (new_poem, seed), 0)])
            return toReturn
        
        # Branching calls
        # -------------------------------------------
        if self.probabilistic:
            result = {}
        else:
            result = []
        print poem #comment out if you want to see the poem being constructed

        if (poem.isFirst()):
            #print "poem isFirst so we get new sentence seeds"
            #This is the number of starting seeds this returns
            for x in range(numSeeds):
                first_seed = []
                for y in range(self.ngrams - 1):
                    first_seed.append('-BEGIN-')
                startWord = util.weightedRandomChoice(self.grammar.begin_map)
                #print "startWord is: ", startWord
                first_seed.append(startWord)
                seed = tuple(first_seed)
                #print "seed is: ", seed
                new_poem = copy.deepcopy(poem)
                curr = new_poem.getLine()
                if curr:
                    if curr.add(startWord):
                        #print "added seed potentially"
                        #time.sleep(5)
                        if not curr: #line has been finished
                            if curr.propagator:
                                for line_i in curr.paired_indices:
                                    if new_poem[line_i].constraint == "": #line has no previous constraint
                                        new_poem[line_i].constraint = startWord
                            new_poem.iterate()
                        if self.probabilistic:
                            result[(startWord, (new_poem, seed), self.grammar.begin_map[startWord])] = self.grammar.begin_map[startWord]
                        else:
                            result.append((startWord, (new_poem, seed), self.grammar.begin_map[startWord]))

        # IMPORTANT NOTE
        # For every successor word, consider all possible children nodes.
        # Pruning to meet rhyming and syllabic constraints of actions needs to be
        # performed here. There is no error checking in the Line or Poetry objects.
        # The rhyming word needs to be passed back and forth between Poetry and Line
        # objects once they are completed (not implemented)
        else:
            if seed in self.grammar.word_map:
                for word, frequency in self.grammar.word_map[seed].iteritems(): #CONSIDER ALL POSSIBLE BRANCHES
                # word: the word that follows the current seed given the n-gram model
                # frequency: the number of times that that word occurs after the given seed
                    if (not(word == '-BEGIN-')):
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
                                if self.probabilistic:
                                    result[(word, (new_poem, new_seed), cost)] = cost
                                else:
                                    result.append((word, (new_poem, new_seed), cost))
        # Idea: sort by descending frequencies so that it looks down more likely paths first
        # or make the ordering probabilistic
        if self.probabilistic:
            toReturn = []
            resultLength = len(result.keys())
            for _ in range(resultLength):
                toAdd = util.weightedRandomChoice(result)
                toReturn.append(toAdd)
                del result[toAdd]
            return toReturn
        else:
            result.sort(key=operator.itemgetter(2), reverse=True)
            return result

#########################################################################
# MAIN EXECUTION
#########################################################################

# Example usage:
# python generator.py -n 2 -f "lyrics/eminem.txt" -o 4
print "[ ] Reading corpus file..."
corpus = Corpus(options.filename)
corpus.analyze(options.ngrams, options.source)
#print corpus.word_map
print "[ ] Finished reading corpus, n-gram model generated."
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
parameters = [(10, pairs) for _ in range(8)] #stub, assumed 10 syllables (words) per line
grammar = Grammar(corpus.frequency_map, corpus.word_map, corpus.begin_map)


for i in range(options.npoems):
    poem = Poetry(parameters, options.sentenceLength)
    problem = PoetrySearchProblem(poem, grammar, options.ngrams, options.probabilistic, options.beginseeds)

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
