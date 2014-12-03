# coding: UTF-8
from optparse import OptionParser
import sys


#IPA defined vowels 
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
	
def rhymes(word1, word2):
	if word1 not in d or word2 not in d:
		# heuristic
		return (word1[-3:] == word2[-3:] and word1 != word2)
	else:
		if word1 == word2:
			return False
		if d[word1][1] == d[word2][1]:
			return True
		else:
			return False

d = {}
with open('IPA_Dict.txt') as f:
	for line in f:
		temp = line.replace(',', '').split()
		print temp
		d[temp[0]] = (temp[1], rhymeVowel(temp[1]), numSyllables(temp[1]))
print rhymes(sys.argv[1], sys.argv[2])




