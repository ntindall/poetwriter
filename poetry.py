import util

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
        syllabic_count = util.getSyllables(word)
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