# FILE: generator.py
# ---------------------------------
# Main generator script

#STD LIBRARIES
from optparse import OptionParser
import  math, random, copy, operator, time, numpy

#FILES
import searchutil, util
from poetry import * 
from grammar import *

# Parse the command line string and behave appropriately 
if __name__ == '__main__':
    parser = OptionParser()

    # Order of the n gram model
    parser.add_option('-n', '--n-gram', type='int', dest='ngrams', default=1)

    # Corpus file, used to train the language model
    parser.add_option('-f', '--file', dest='filename', default="corpora/whitman.txt")

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
    parser.add_option('-b', '--begin-seeds', type='int', dest='beginseeds', default=3)

    # The number of children seeds to try before backtracking, selects the r most frequent 
    # children or the first r children seeded (if probabilistic)
    parser.add_option('-r', '--branching', type='int', dest='branching')

    # The type of poetry to output (options: sonnet, haiku, eight, octave, quad)
    parser.add_option('-t', '--type', dest='type', default='quad')

    # Verbosity of the generator module
    parser.add_option('-v', '--verbose', type='int', dest='verbose', default=0)
    (options, args) = parser.parse_args()

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
                toReturn.append((seed, (new_poem, seed), 0))
            return toReturn
        
        # Branching calls
        # -------------------------------------------
        if self.probabilistic:
            result = {}
        else:
            result = []
        if (options.verbose > 0):
            print poem 

        if (poem.isFirst()):
            if (options.verbose > 1):
                print "[ ] poem isFirst so we get new sentence seeds"
            #This is the number of starting seeds this returns
            for x in range(numSeeds):
                first_seed = []
                for y in range(self.ngrams - 1):
                    first_seed.append('-BEGIN-')
                startWord = util.weightedRandomChoice(self.grammar.begin_map)
                first_seed.append(startWord)
                seed = tuple(first_seed)
                new_poem = copy.deepcopy(poem)
                curr = new_poem.getLine()
                if curr:
                    if curr.add(startWord):
                        if (options.verbose > 1):
                            print "[ ] reseeded grammar with: ", startWord
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
                                if (options.verbose > 1):
                                    print "[ ] added seed ", startWord
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
            if (options.branching):
                return toReturn[:options.branching]
            return toReturn
        else:
            result.sort(key=operator.itemgetter(2), reverse=True)
            if (options.branching):
                return result[:options.branching]
            return result

#########################################################################
# MAIN EXECUTION
#########################################################################

# Example usage:
# python generator.py -n 2 -f "lyrics/eminem.txt" -o 4
# python generator.py -f corpora/shakespeare.txt -n 2 -o 1 -s rap -l 2 -b 10 -t octave -r 3 -p 1
# python generator.py -f corpora/shakespeare.txt -n 2 -o 2 -l 2 -b 10 -t eight -r 3 -p 1 -v 1
# python generator.py -f corpora/shakespeare.txt -n 3 -o 5 -l 2 -b 10 -t eight -r 3 -p 1 -v 1

print "[ ] Reading corpus file..."
corpus = Corpus(options.filename)
corpus.analyze(options.ngrams, options.source)
if (options.verbose > 2):
    print corpus.word_map
print "[ ] Finished reading corpus, n-gram model generated."

# ABOUT: THE PAIR LIST
# 
# Assumption: pairs are increasing (propagator, receiver) order, can't propagate to self. 
# Chains must be fully realized, i.e. [(0,1), (0,7), (6,7)] is invalid, while [(0,1), (0,6),(0,7),(6,7)]
# is valid (though the last item is redundant). [(0,1),(0,5),(2,3),(3,4),(5,6),(6,7)] will work, while 
# [(0,1),(0,7),(2,3),(3,4),(5,6),(6,7)], will yield errors, better to be consistent:
# [(0,1), (0,5), (0,6),(0,7),(2,3),(2,4)]
#
# Successive chains are safe, while separated ones require more tentative handling

if options.type == 'sonnet':
    pairs = [(0,2),(1,3),(4,6),(5,7),(8,10),(9,11),(12,13)] #ABABCDCDEFEFGG
    parameters = [(10, pairs) for _ in range(14)]
if options.type == 'haiku':
    parameters = [(5,[]),(7,[]),(5,[])]
if options.type == 'eight': #eight lines of iambic tetameter AA BB CC DD
    pairs = [(0,1),(2,3),(4,5),(6,7)]
    parameters = [(8, pairs) for _ in range(8)]
if options.type == 'octave': #eight lines of iambic pentameter ABBA CDDC
    pairs = [(0,3),(1,2),(4,7),(5,6)]
    parameters = [(10, pairs) for _ in range(8)]
if options.type == 'quad':
    pairs = [(0,1), (1,2), (2,3)]
    parameters = [(10, pairs) for _ in range(4)]

#Initialize grammar
grammar = Grammar(corpus.frequency_map, corpus.word_map, corpus.begin_map)

if (options.verbose > 2):
    print "[ ] Pairs: ", pairs
    print "[ ] Parameters: ", parameters

# Keep track of every poem written
written = []

for i in range(options.npoems):
    start = time.time()
    poem = Poetry(parameters, options.sentenceLength)
    problem = PoetrySearchProblem(poem, grammar, options.ngrams, options.probabilistic, options.beginseeds)

    #DEPTH FIRST SEARCH
    bts = searchutil.DepthFirstSearch(verbose=1)
    bts.solve(problem)
    end = time.time()
    print ""
    written.append((bts.solution, bts, end - start))
    if bts.solution:
        solution, final_seed = bts.solution
        print "RESULT"

        print solution
    else:
        print "NO SOLUTION FOUND"

#Print generated poems 
if (options.npoems > 1):
    times = []
    explored = []
    for solution, bts, time in written: #includes times of unfound solutions
        num_states_explored = bts.stats()
        if solution[0]:
            print "Time = %f" % time
            print ""
            print solution[0]
            print ""
        times.append(time)
        explored.append(num_states_explored)
    print "[ ] attempted to satisfy %d poems" % options.npoems
    print "[ ] %d found" % sum(1 if t[0] else 0 for t in written)
    print "[ ] total time = %f" % sum(times)
    print "[ ] mean t = %f" % numpy.average(times)
    print "[ ] median t = %f" % numpy.median(times)
    print "[ ] stdev t = %f" % numpy.std(times)
    print "[ ] mean s = %f" % numpy.average(explored)
    print "[ ] median s = %f" % numpy.median(explored)
    print "[ ] stdev s= %f" % numpy.std(explored)
