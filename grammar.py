import util

# Grammar object
# ------------------------
# Stores data about the way words and successors are
# related based on a corpus file
class Grammar(object):
    # --------------
    # Constructor for the Grammar class.
    def __init__(self, fmap, wmap):
        self.frequency_map = fmap
        self.word_map = wmap
        self.seed_key = None
        self.seed = ""
        self.past_seed = False

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
