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

class grammar(object):
    # --------------
    # Constructor for the Line class.
    def __init__(self, fmap, wmap):
        self.frequency_map = fmap
        self.word_map = wmap
        self.seed_key = None
        self.seed = ""

    def next(self):
        if self.seed_key == None:
            self.seed_key = weightedRandomChoice(self.frequency_map)
            for i in range(len(self.seed_key)):
                self.seed += self.seed_key[i] + " "
            self.seed.strip() #trim whitespaces
            return self.seed
        if self.seed_key not in self.word_map:
            return None
        else: 
            next = weightedRandomChoice(self.word_map[self.seed_key])
            broken_seed = self.seed.split()
            broken_seed.pop(0)
            broken_seed.append(next)
            self.seed = ' '.join(broken_seed)
            self.seed.strip()
            self.seed_key = tuple(broken_seed)
            return next


class Line (object):
    # --------------
    # Constructor for the Line class.
    def __init__(self, syllables, pairs):
        self.syllables = syllables #while syllables > 0
        self.pairs = pairs
        self.words = []
        self.last = ""

    # Function: nonzero
    # --------------
    # Allow Poetry objects to be evaluated as booleans
    def __nonzero__(self):
        return (self.syllables != 0)

    def add(self, word):
        #check with pairs
        syllabic_count = getSyllables(word)
        if (self.syllables > syllabic_count):
            self.words.append(word)
            self.syllables -= syllabic_count
            return True
        if (self.syllables == syllabic_count):
            self.words.append(word)
            self.syllables -= syllabic_count
            self.last = word
            return True
        else:
            return False 

    def toString(self):
        return ' '.join(self.words)


class Poetry (object):
    # Function: Init
    # --------------
    # Constructor for the Poetry class.
    def __init__(self, lineParams):
        #lineParams are (# syllable, [pair]) tuples
        #pairs are indexed by position in lineParams (and thus in self.lines)
        self.lines = []
        for param in lineParams:
            self.lines.append(Line(param[0],param[1]))
        self.currentLine = 0
        self.numLines = len(lineParams)

    # Function: nonzero
    # --------------
    # Allow Poetry objects to be evaluated as booleans
    def __nonzero__(self):
        return (self.currentLine == self.numLines)

    def iterate(self):
        self.currentLine += 1

    def getLine(self):
        return self.lines[self.currentLine]

    def format(self):
        output = ""
        for line in self.lines:
            output += line.toString() + '\n'
        return output

        