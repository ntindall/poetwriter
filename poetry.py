import util

# The current state of a given poem
class Poetry (object):
    # Function: Init
    # --------------
    # Constructor for the Poetry class.
    def __init__(self, lineParams):
        # lineParams are (# syllable, [pair]) tuples
        # pairs are indexed by position in lineParams (and thus in self.lines)
        self.lines = []
        for i, param in enumerate(lineParams):
            self.lines.append(Line(i, param[0],param[1]))
        self.currentLine = 0
        self.numLines = len(lineParams)

    # Function: nonzero
    # --------------
    # Allow Poetry objects to be evaluated as booleans
    def __nonzero__(self):
        return (self.currentLine == self.numLines)

    # Function: getitem
    # --------------
    # Allow poetry lines to be accesed by their line index, i.e.
    # firstLine = poem[0] = self.lines[0]
    def __getitem__(self, key):
        return self.lines[key]

    # Function: __str__
    # --------------
    # Formats poetry to be printed to console
    def __str__(self):
        output = ""
        for line in self.lines:
            output += line.toString() + '\n'
        return output

    # Function: iterate
    # --------------
    # Moves to next line
    def iterate(self):
        self.currentLine += 1

    # Function: getLine
    # --------------
    # Returns the line currently being edited
    def getLine(self):
        if not self.lines[self.currentLine]: #current line not eligible
            print "updating"
           # self.currentLine += 1
        if self.currentLine == self.numLines:
            return None
        return self.lines[self.currentLine]

# The current state of a given line of poetry
class Line (object):
    # --------------
    # Constructor for the Line class.
    def __init__(self, i, syllables, pairs):
        self.number = i
        self.goal = syllables
        self.syllables = syllables #while syllables > 0
        self.pairs = pairs
        self.words = []
        self.last = ""
        self.propogator = False #line propogates a rhyme constraint
        self.receiver = False #line receives a rhyme constraint
        for tup in pairs:
            if tup[0] == i:
                self.propogator = True
            if tup[1] == i:
                self.receiver = True

    # Function: nonzero
    # --------------
    # Allow Line objects to be evaluated as booleans
    def __nonzero__(self):
        return (self.syllables != 0)

    # Function: __str__ 
    # --------------
    # Converts to string
    def __str__(self):
        return ' '.join(self.words)

    # Function: add
    # --------------
    # Adds a new word to the line, does not add to line if the
    # word does not 
    def add(self, word):
        #check with pairs (stub)
        syllabic_count = util.getSyllables(word)
        # word fits with room to spare
        if (self.syllables > syllabic_count):
            self.words.append(word)
            self.syllables -= syllabic_count
            return True
        # word fits, is final word
        if (self.syllables == syllabic_count):
            self.words.append(word)
            self.syllables -= syllabic_count
            self.last = word
            return True
        # word doesn't fit
        else:
            return False 

    def toString(self):
        return ' '.join(self.words)