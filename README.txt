TO DOWNLOAD FINAL PDF WRITEUP:
https://github.com/ntindall/poetwriter/blob/master/tex/writeup.pdf?raw=true

---------------------------------------------------------------
- FINAL PROJECT: POETWRITER                                   -
---------------------------------------------------------------
- Mathieu Rolfo, Shalom Rottman-Yang, Nathan Tindall          -
- CS221 Autumn 2014                                           -
- Stanford University                                         -
- Prof Percy Liang                                            -
- TA Aparna Krishnan                                          -
- http://web.stanford.edu/class/cs221/                        -
- 12 December 2014                                            -
---------------------------------------------------------------

---------------------------------------------------------------
- CONTENTS                                                    -
---------------------------------------------------------------
* INTRODUCTION
* USAGE
* EXAMPLE
* FILES
* ALGORITHMIC APPROACH
* DATA

---------------------------------------------------------------
- INTRODUCTION                                                -
---------------------------------------------------------------
Our task for this project was to design a framework for poetry 
generation that allows a human to give a corpus as input and 
specify formal constraints, and have our intelligent creation 
generate novel, semantically meaningful poetry meeting those 
constraints. Our algorithm has special optimizations for the 
corpora of rap artists in an attempt to generate rap-styled 
poetry; however, the general case of the problem is one of 
poetic generation. In this project, our constraints are on the 
syllable counts within lines and the rhyming patterns between lines. 

---------------------------------------------------------------
- USAGE                                                       -
---------------------------------------------------------------
The algorithm can be invoked by running generator.py, with the 
following flags:
* (-n), default 1
  Order of the n gram model
* (-f), default "whitman.txt"
  Corpus file, used to train the language model.
* (-o), default 3
  The number of poems to output
* (-l), default 1
  The phrase length (number of lines that the n-gram wraps 
  around before reseeding).
* (-s)
  The type of corpus, in order to facilitate corpus cleanup
* (-p), default true
  Whether the model is probabalistic when selecting actions (if 
  not selected, chooses more frequent seeds first
* (-b), default 3
  The number of initial seeds to try before backtracking 
  (when the grammar is reseeded)
* (-r)
  The number of children seeds to try before backtracking, 
  selects the r most frequent children or the first r children
  randomly selected (if probabilistic).
* (-t), default quad
  The type of poetry to output (options: sonnet, haiku, eight, 
  octave, quad)
* (-v), default 0
  The verbosity of the program. A value of 1 or higher lets you
  watch the algorithm's search process.

---------------------------------------------------------------
- EXAMPLE                                                     -
---------------------------------------------------------------
# python generator.py -n 2 -f lyrics/eminem.txt -o 4
# python generator.py -f corpora/shakespeare.txt -n 2 -o 1 -s rap -l 2 -b 10 -t octave -r 3 -p 1
# python generator.py -f corpora/shakespeare.txt -n 2 -o 2 -l 2 -b 10 -t eight -r 3 -p 1 -v 1
# python generator.py -f corpora/chance.txt -n 2 -o 5 -l 2 -b 10 -t eight -r 3 -p 1 -v 1

---------------------------------------------------------------
- FILES                                                       -
---------------------------------------------------------------
baseline.py: Algorithmic baseline
* Trains language model with user specified corpus (-f), number
  of poems generated (-o), and model order (-n).
* Formed algorithmic backbone and framework on which to improve
* Archaic

generator.py: Main execution
* Run from command line to generate poetry, parses command line
  to orient hyperparameters of algorithm as specified by the
  user
* See "Usage" below for invocation
* Instantiates a corpus and runs n gram analysis
* Determines parameters of the poetry object
* Instantiates a grammar (language model) based upon the corpus
* Runs search algorithm
* Prints statistics 

grammar.py: Corpus and Grammar Classes
* The Corpus class performs n gram analysis, generating a
  frequency map, a word map, and a beginning word map.
* The Grammar class is instantiated from the data structures
  of the Corpus model, and is general enough to work in a non
  search oriented implementation.

new_word_data.p: Dictionary
* Generated using the Moby Pronunciation Dictionary and Moby Part of Speech Dictionary, the largest public domain dictionaries of their kinds with over 100,000 entries. 
* Our heuristic for syllable count is the number of unstressed vowels.
* Our heuristic for rhyming is the last vowel in the word and any trailing consonants
* Keys: words in plaintext
* Values: (IPA Transcription, IPA Suffix, Number of Syllables,
           Part of Speech, isNotPrepOrArticle)

poetry.py: Poetry and Line Classes
* Poetry class is comprised of Line classes. Evaluation returns
  true when all inter- and intra-line constraints have been 
  satisfied.
* Line class stores a list of the current words in the line, the current syllable count, and inter-line constraints it received or needs to propagate (which lines it must rhyme with)

rap_genius_scraper.rb: A scraper for rapgenius.com
* Used to aggregate rap corpora
* Takes two command line arguments: the song id of the desired artists' song, and the name of the output file.

searchutil.py: Search Algorithms
* Houses UCS and DFS implementations
* DFS code tweaked to return as soon as solution is found, 
  rather than searching all paths to find the best solution 
  based upon some cost.

util.py: Utility functions
* clean(string): Used to strip down corpus of a-zA-Z0-9 chars
* weightedRandomChoice(weightDict): Chooses item from a pool
* isNoun(word): Returns True if word is a noun (accessess 
  pickle dict)
* isNotPrepOrArticle(word): Returns True if word is not prep or
  article (acesses pickle dict)
* numSyllables(ipa_reading): Returns the number of syllables in
  an IPA Unicode String
* getSyllables(word): Returns the number of syllables in a word
  (acesses pickle dict)
* rhymeVowel(ipa_reading): Algorithm for determining IPA suffix
* rhyme(word1, word2): returns True if two words rhyme, acesses
  IPA dictionary
* Loads the pickle dictionary when imported

---------------------------------------------------------------
- ALGORITHMIC APPROACH                                        -
---------------------------------------------------------------
Our algorithm uses depth first search in order to solve the 
constraints of the poetry object. We have defined the search
problem in the following manner:

* startState: (current poem state, current seed)
* isGoal(state): state[0] is a completed poem
* succAndCost(state): performs search over the language model
  by iteratively re-seeding corpus in an attempt to satisfy
  the Poetry class. Words are added to lines, and paths dis-
  carded if they break the constraints of the model.

---------------------------------------------------------------
- Data		            	                              -
---------------------------------------------------------------
eliot.txt
* n=1: Mean time = 91.66s; Median time = 66.84s; Mean states = 4773.75; 
Median states = 3547.5; Completion rate = 100%; Semantic score = 1.35
* n=2: Mean time = 0.21s; Median time = .18s; Mean states = 163.05; 
Median states = 111.5; Completion rate = 0%; Semantic score = N/A
* n=3: Mean time = 0.09s; Median time = 0.09s; Mean states = 16.5; 
Median states = 16; Completion rate = 0%; Semantic score = N/A

whitman.txt
* n=1: Mean time = 1352.69s; Median time = 165.73s; Mean states = 4959; 
Median states = 532; Completion rate = 100%; Semantic score = 1.66
* n=2: Mean time = 18.203s; Median time = 12.101; Mean states = 1705.6; 
Median states = 1184; Completion rate = 100%; Semantic score = 2.45
* n=3: Mean time = 1.548s; Median time = 1.415s; Mean states = 80.2; 
Median states = 60.5; Completion rate = 0%; Semantic score = N/A

shakespeare.txt
* n=1: Mean time = 6480s; Median time = 6480s; Mean states = 9333.80; 
Median states = 397; Completion rate = 100%; Semantic score = 1.20
(Only five poems generated after 9 hour run time; only these data points reported)
* n=2: Mean time = 81.918s; Median time = 30.761s; Mean states = 3784; 
Median states = 1305.05; Completion rate = 100%; Semantic score = 2.18
* n=3: Mean time = 14.96s; Median time = 13.66s; Mean states = 1220.90; 
Median states = 1023; Completion rate = 45%; Semantic score = 3.22











