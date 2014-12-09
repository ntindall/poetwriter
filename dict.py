import pickle, sys

d = pickle.load(open("word_data.p", "rb"))

def isNoun(word):
    if word in d.keys():
        return u'N' in d[word][3]

print isNoun(sys.argv[1]), d[sys.argv[1]]