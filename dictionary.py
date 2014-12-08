# coding: UTF-8
import random
import re
import sys
import codecs
import pickle





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

#must be unicode!!!! 
vowels = u'æɑəɪieɛɝɚɐʌʊuoɔa' #ɹ


def numSyllables(ipa_reading):
    num = 0
    for i in range(len(ipa_reading)):
        if ipa_reading[i] in vowels:
            num += 1

    return num

# Called in poetry.py
def getSyllables(word):
    if word not in d:
        # heuristic
        return max(len(word) / 3, 1)
    else:
        return d[word][2]

#ipa_reading is a unicode string
def rhymeVowel(ipa_reading):
    #removes stressing on syllables; can add back later for more fine-grained rhyme
    stripped_ipa = ipa_reading.replace('\'', '')

    # get the position of the last vowel
    for i in reversed(range(len(stripped_ipa))): 
        if stripped_ipa[i] in vowels:
            break

    #print ":".join("{:02x}".format(ord(c)) for c in stripped_ipa), stripped_ipa
    #print ":".join("{:02x}".format(ord(c)) for c in stripped_ipa[i::]), stripped_ipa[i::]

    # return suffix starting at the last vowel: the characteristic of whether a word rhymes depends on the last 
    # vowel and the following consonants
    if (len(stripped_ipa)-i < 3 and i != 0):
        #print 'POOP'
        return stripped_ipa[i-1::]
    else:
        #print 'DIARRHEA'
        return stripped_ipa[i::]







	
def rhymes(word1, word2):
	if word1 not in d or word2 not in d:
		# heuristic
		return (word1[-3:] == word2[-3:] and word1 != word2)
	else:
		print d[word1], d[word2]
		print word1, d[word1][0], d[word1][1],d[word1][2]
		print word2, d[word2][0], d[word2][1],d[word2][2]
		if word1 == word2:
			return False
		if d[word1][1] == d[word2][1]:

			return True
		else:
			return False

d = {}
with codecs.open('IPA_Dict.txt', encoding='utf-8') as f:
    for line in f:
        temp = line.replace(',', '').split()
        d[temp[0]] = (temp[1], rhymeVowel(temp[1]), numSyllables(temp[1]))


rhymes(sys.argv[1], sys.argv[2])





