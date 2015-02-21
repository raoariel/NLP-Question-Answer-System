import nltk


text = nltk.word_tokenize(open(file.read()))
#This is the built in pos tagger
tagged = nltk.pos_tag(text)
#this uses bigrams to tag based on training sentences
bigram_tagger = nltk.BigramTagger(train_sents)
bigram_tagger.tag(text)
#this line would tag Named entities
nltk.ne_chunk(tagged)
#converts a list of words into list of bigrams
list(bigrams([list]))

#basic chunking of NPs
grammar = "NP: {<DT>?<JJ>*<NN>}"
cp = nltk.RegexpParser(grammar)
result = cp.parse(tagged)





