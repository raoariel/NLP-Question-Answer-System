# File must be in stanfordCoreNLP directory
# Dependencies must be installed; other than stanfordCoreNLP, availible via pip install
# Directories may need to be changed; currently hard coded


from parseNLP import Parse

# required parameter: fileName ("*.htm")
# optional parameters: textRange (int: size of text block to chuck in
#                      dataDir (str: directory of data relative to current folder (ie coreNLP))
#                                    - see code for current default
file = Parse("languages_a1.htm")

# returns nested list of parse tree and raw string as tuple
(parseTree, rawSentence) = file.getContent()

# Note: parseNLP is non-deterministic
# file.getContent() => should generally return new sentence but it is not guaranteed
