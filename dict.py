import pickle, sys

d = pickle.load(open("word_data.p", "rb"))
new_dict = {}

def isNotPrepOrArticle(word):
    return not (u'P' in d[word][3] or u'D' in d[word][3] or u'I' in d[word][3] or u'C' in d[word][3]) 
    return False;

n = 0
for word in d.keys():
	a, b, c, f = d[word]
	e = isNotPrepOrArticle(word)
	new_dict[word] = (a, b, c, f, e)
	n += 1
	print n, word, new_dict[word]

pickle.dump(new_dict, open("new_word_data.p", "wb"))

#print isNotPrepOrArticle(sys.argv[1]), d[sys.argv[1]]