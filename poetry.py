import util

# The current state of a given poem
class Poetry (object):
    # Function: Init
    # --------------
    # Constructor for the Poetry class.
    def __init__(self, lineParams, sentenceLength):
        # lineParams are (# syllable, [pair]) tuples
        # pairs are indexed by position in lineParams (and thus in self.lines)
        self.lines = []
        for i, param in enumerate(lineParams):
           self.lines.append(Line(i, param[0],param[1], sentenceLength))
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
        if self.currentLine == self.numLines:
            return None
        return self.lines[self.currentLine]

    # Function: isFirst
    # --------------
    # Returns whether the poem is at the first word of a sentence
    def isFirst(self):
        return self.lines[self.currentLine].isFirst()

# The current state of a given line of poetry
class Line (object):
    # --------------
    # Constructor for the Line class.
    def __init__(self, i, syllables, pairs, sentenceLength):
        self.number = i
        self.goal = syllables
        self.syllables_left = syllables #while syllables > 0
        self.paired_indices = []
        self.words = []
        self.last = ""
        self.sentenceLength = sentenceLength

        self.constraint = ""
        self.propagator = False #line propogates a rhyme constraint
        self.receiver = False #line receives a rhyme constraint
        for tup in pairs:
            if tup[0] == i:
                self.propagator = True
                self.paired_indices.append(tup[1])
            if tup[1] == i:
                self.receiver = True


    # Function: nonzero
    # --------------
    # Allow Line objects to be evaluated as booleans
    def __nonzero__(self):
        return (self.syllables_left > 0)

    # Function: __str__ 
    # --------------
    # Converts to string
    def __str__(self):
        return ' '.join(self.words)

    # Function: isFirst
    # --------------
    # Returns whether the line is at the first word of a sentence
    def isFirst(self):
        if ((self.number % self.sentenceLength == 0) and (len(self.words) == 0)):
            return True
        else:
            return False

    # Function: isLast
    # --------------
    # Returns whether the line is the last line of a sentence
    def isLast(self):
        if (self.number % self.sentenceLength == self.sentenceLength - 1):
            return True
        else:
            return False

    # Function: add
    # --------------
    # Adds a new word to the line, does not add to line if the
    # word does not fit constraints
    def add(self, word):
        #check with pairs (stub)
        syllabic_count = util.getSyllables(word)
        #print "word has ", syllabic_count, " syllables"
        #print "the line has ", self.syllables_left, "syllables left"
        # word fits with room to spare
        if (self.syllables_left > syllabic_count):
            #print "word fits with room to spare"
            self.words.append(word)
            self.syllables_left -= syllabic_count
            return True
        # word fits, is final word
        if (self.syllables_left == syllabic_count) and util.isNotPrepOrArticle(word):
            #print "word fits"
            if self.receiver:
                #print "word is a receiver"
                if util.rhyme(word, self.constraint):
                    #print "rhyme found"
                    self.words.append(word)
                    self.syllables_left -= syllabic_count
                    self.last = word
                    print word, 'is a noun'
                    return True
                else: 
                    #print "no rhyme here"
                    return False
            #Curr is not receiver, proceed as normal
            self.words.append(word)
            self.syllables_left -= syllabic_count
            self.last = word
            return True
        # word doesn't fit
        else:
            return False 

    def toString(self):
        return ' '.join(self.words)
