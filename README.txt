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
  to 
* Instantiates a corpus and runs n gram analysis
* Determines aparameter

grammar.py
new_word_data.p
poetry.py
rap_genius_scraper.rb
README.txt
searchutil.py
util.py

---------------------------------------------------------------
- ALGORITHMIC APPROACH                                        -
---------------------------------------------------------------

---------------------------------------------------------------
- USAGE                                                       -
---------------------------------------------------------------