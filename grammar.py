# FILE: util.py 
# ---------------------------------
# Houses the Corpus and Grammar classes

import util
import string
import glob
from collections import Counter

# Corpus object
# ------------------------
# Opens corpus file and collects data about it
# Right now, just does n gram analysis
class Corpus(object):
    def __init__(self, name):
        self.file = open(name, 'r')
        self.frequency_map = Counter()
        self.word_map = {}
        self.begin_map = Counter()
        self.numlines = 0
    
    # n-gram algorithm

    # Consider a second analyze algorithm with:
        # a) no line break characters
        # b) 

    def analyze(self, n, source):
        queue = []
        for line in self.file:
            self.numlines += 1
            line = util.clean(line)
            words = queue
            #Assumes each line in the corpus is a separate 'sentence'
            for _ in range(n):
                words.append('-BEGIN-')
            words.extend(line.split()) # current words to be considered
            if line.split():
                self.begin_map[line.split()[0]] += 1
            if ((source == "rap") and ((line == "") or (string.find(line, "verse") != -1) or (string.find(line, "hook") != -1) or (string.find(line, "bridge") != -1))):
                words = []
            queue = [] # reset queue upon reading new line
            while (len(words) > n):
                key = []
                for i in range(n):
                    key.append(words[i])
                k = tuple(key)
                self.frequency_map[k] += 1
                if k not in self.word_map:
                    self.word_map[k] = Counter({words[i + 1]:1})
                else:
                    self.word_map[k].update({words[i + 1]: 1})
                words.pop(0)
            [queue.append(word) for word in words] #add leftover words to queue

    def normalize(self):
        for key in self.word_map:
            total = sum(self.word_map[key].values())
            for k in self.word_map[key]:
                word_map[key][k] = word_map[key][k] / float(total)

# Grammar object
# ------------------------
# Stores data about the way words and successors are
# related based on a corpus file
class Grammar(object):
    # --------------
    # Constructor for the Grammar class.
    def __init__(self, fmap, wmap, bmap):
        self.frequency_map = fmap
        self.word_map = wmap
        self.seed_key = None
        self.seed = ""
        self.past_seed = False
        self.begin_map = bmap

    # Gets the next word from the grammar predictor
    # (Implemented as n-gram)
    def next(self):
        # If no seed, pick a seed and return seed
        if self.seed_key == None: 
            self.seed_key = util.weightedRandomChoice(self.frequency_map)
            for i in range(len(self.seed_key)):
                self.seed += self.seed_key[i] + " "
            self.seed = self.seed.strip() #trim whitespaces
            return self.seed
        # Grammar is stuck
        if self.seed_key not in self.word_map:
            return None
        # Pick a random choice from the successors of seed
        # Mostly deterministic except for large corpora
        else: 
            next = util.weightedRandomChoice(self.word_map[self.seed_key])
            return next

    # Iterates seed
    def update(self, next):
        # Only should update after the second call to update
        if not self.past_seed:
            self.past_seed = True
        else:
            broken_seed = self.seed.split()
            broken_seed.pop(0)
            broken_seed.append(next)
            self.seed = ' '.join(broken_seed).strip()
            self.seed_key = tuple(broken_seed)

print "[ ] Reading corpus file in grammar..."
files = glob.glob('corpora/*.txt')

for txt in files:
    
    corpus = Corpus(txt)
    corpus.analyze(2, 'rap')
    print txt, ', num keys =', len(corpus.word_map.keys()), ', num lines =', corpus.numlines
