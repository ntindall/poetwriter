import util

class Grammar(object):
    # --------------
    # Constructor for the Grammar class.
    def __init__(self, fmap, wmap):
        self.frequency_map = fmap
        self.word_map = wmap
        self.seed_key = None
        self.seed = ""

    def next(self):
        if self.seed_key == None:
            self.seed_key = util.weightedRandomChoice(self.frequency_map)
            for i in range(len(self.seed_key)):
                self.seed += self.seed_key[i] + " "
            self.seed = self.seed.strip() #trim whitespaces
            return self.seed
        if self.seed_key not in self.word_map:
            return None
        else: 
            next = util.weightedRandomChoice(self.word_map[self.seed_key])
            broken_seed = self.seed.split()
            broken_seed.pop(0)
            broken_seed.append(next)
            self.seed = ' '.join(broken_seed)
            self.seed_key = tuple(broken_seed)
            return next