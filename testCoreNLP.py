from corenlp import *
import json

corenlp = StanfordCoreNLP()
sentence = "Bob is a dog who loves cats. Emily is a carrot and she hates bongo drums."

corefs = json.loads(corenlp.parse(sentence))["coref"]
print sentence

print corefs

corefDict = dict()
for references in corefs:
    coreferent = references[0][1][0]
    refs = []
    for tuple in references:
        pronoun = tuple[0][0]
        sentenceNum = tuple[0][1]
        refs.append((pronoun, sentenceNum))
    corefDict[coreferent] = refs
    
print corefDict

