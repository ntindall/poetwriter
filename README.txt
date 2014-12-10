README.txt

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
* FILES
* ALGORITHMIC APPROACH
* USAGE

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
syllable counts of lines and the rhyming patterns between lines. 

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
* Instantiates a corpus and runs n gram analysis.
* Determines parameters of the poetry object
* Instantiates a grammar (language model) based upon the corpus
* Runs search algorithm
* Prints statistics 

grammar.py: Corpus and Grammar Classes
* The Corpus clas performs n gram analysis, generating a
  frequency map, a word map, and a beginning word map.
* The Grammar class is instantiated from the data structures
  of the Corpus model, and is general enough to work in a non
  search oriented implementation.

new_word_data.p: Dictionary
* Keys: words in plaintext
* Values: (IPA Transcription, IPA Suffix, Number of Syllables,
           Part of Speech, isNotPrepOrArticle)

poetry.py: Poetry and Line Classes
* Poetry class is comprised of Line classes. Evaluation returns
  true when all inter- and intra-line constraints have been 
  satisfied.
* Line class is a 

rap_genius_scraper.rb: A scraper for rapgenius.com
* Used to aggregate rap corpora

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
- USAGE                                                       -
---------------------------------------------------------------

* (-n), default 1
  Order of the n gram model
* (-f), default "whitman.txt"
  Corpus file, used to train the languaeg model
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
  The type of poetry to output (options: sonnet, haiku, eight, octave, quad)
* (-v), default 0
  The verbosity of the program