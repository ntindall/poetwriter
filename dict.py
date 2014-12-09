import pickle, sys

d = pickle.load(open("word_data.p", "rb"))

def isNoun(word):
    if word in d.keys():
        return u'N' in d[word][3]

def isNotPrepOrArticle(word):
    if word in d.keys():
        return not (u'P' in d[word][3] or u'D' in d[word][3] or u'I' in d[word][3])
    return False;

print isNotPrepOrArticle(sys.argv[1]), d[sys.argv[1]]