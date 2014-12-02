import random
import re


# Used to strip down corpus of non a-z,A-Z,0-9 chars
# and defaults to lower case. 
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

# Called in poetry.py
def getSyllables(word):
    #boilerplate
    #print len(word)
    return max(len(word) / 3, 1)

def rhyme(word1, word2):
    return (word1[-3:] == word2[-3:]) and (word1 != word2)


#     if word1 == "" or word2 == "": return True #no constraint
#     last_vowel1 = ""
#     last_vowel2 = ""

#     for z in word1[::-1]:
#         if z in 'aeiou':
#             last_vowel1 = z
#             break

#     for y in word2[::-1]:
#         if y in 'aeiou':
#             last_vowel2 = y
#             break
#     return last_vowel2 == last_vowel1