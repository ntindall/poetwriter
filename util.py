import random
import re

def clean(string):
    mixed_case = re.sub(r'[^\w\s-]', '', string)
    return mixed_case.lower()

# Takes a random choice based on a weight dict
# is deterministic for small corpora 
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
    #boilerplate
    return 2 #weightedRandomChoice({2:1,1:1}) 
    # flexible system, but given flatness of weight dict , 
    # just re-adds last word on line until this function returns
    # 1 rather than 2 (i.e. 2 2 2 1 2 --> 2 2 2 1 1) but the word added
    # is the same regardless of syllable count. Will cause an issue when syllable
    # counts are deterministic