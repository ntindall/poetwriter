import random

def weightedRandomChoice(weightDict):
    weights = []
    elems = []
    for elem in weightDict:
        weights.append(weightDict[elem])
        elems.append(elem)
    total = sum(weights)
    key = random.uniform(0, total)
    runningTotal = 0.0
    chosenIndex = None
    for i in range(len(weights)):
        weight = weights[i]
        runningTotal += weight
        if runningTotal > key:
            chosenIndex = i
            return elems[chosenIndex]
    raise Exception('Should not reach here')

def getSyllables(word):
    return 1

class Line (object):
    # --------------
    # Constructor for the Poetry class.
    def __init__(self, syllables, pairs):
        self.syllables = syllables #while syllables > 0
        self.pairs = pairs
        self.words = []
        self.last = ""

    def add(self, word):
        syllabic_count = getSyllables(word)
        if (self.syllables > syllabic_count):
            self.words.append(word)
            self.syllables -= syllabic_count
            return True
        if (self.syllables == syllabic_count):
            self.word.append(word)
            self.syllables -= syllabic_count
            self.last = word
            return True
        else:
            return False 


class Poetry (object):
    # Function: Init
    # --------------
    # Constructor for the Poetry class.
    def __init__(self, lineParams):
        #lineParams are (# syllable, [pair]) tuples
        #pairs are indexed by position in lineParams (and thus in self.lines)
        self.lines = []
        for param in lineParams
            lines.append(Line(lineParams[0],lineParams[1]))
        self.numLines = len(lineParams)
        self.complete = False

    # Function: Init
    # --------------
    # Allow Poetry objects to be evaluated as booleans
    def __nonzero__(self):
        return self.complete != False
        
    # Function: Set Prob
    # ------------------
    # Sets the probability of a given row, col to be p
    def setProb(self, row, col, p):
        self.grid[row][col] = p