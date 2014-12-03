# coding: UTF-8
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


vowels = 'æɑəɪieɛɹɝɚɐʌʊuo'


def numSyllables(ipa_reading):
    num = 0
    for i in range(len(ipa_reading)-1):
        if ipa_reading[i] in vowels:
            if i != len(ipa_reading)-1:
                if ipa_reading[i+1] != '\'':
                    num += 1
    return num

def rhymeVowel(ipa_reading):

    #removes stressing on syllables; can add back later for more fine-grained rhyme
    stripped_ipa = ipa_reading.replace('\'', '')

    

    # get the position of the last vowel
    last_vowel_index = -1
    for i in reversed(range(len(stripped_ipa)-1)): 
        if stripped_ipa[i] in vowels:
            break

    # return suffix starting at the last vowel: the characteristic of whether a word rhymes depends on the last 
    # vowel and the following consonants
    return stripped_ipa[i::]

# Called in poetry.py
def getSyllables(word):
    #boilerplate
    #print len(word)
    return max(len(word) / 3, 1)

d = {}
with open('IPA_Dict.txt') as f:
    for line in f:
        temp = line.replace(',', '').split()
        d[temp[0]] = (temp[1], rhymeVowel(temp[1]), getSyllables(temp[1]))

def rhyme(word1, word2):

    if word1 not in d or word2 not in d:
        # heuristic
        return (word1[-2:] == word2[-2:] and word1 != word2)
    else:
        if word1 == word2:
            return False
        if d[word1][1] == d[word2][1]:
            print word1, word2
            return True
        else:
            return False




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