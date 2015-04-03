# Demo for parse & extract modules VERSION 2
# Dependencies: 
#   convert.py  parseNLP.py  extractNLP.py
#   os, sys, re, string, ast, json 
#   nltk, corenlp, random, bs4, collections


from parseNLP import Parse
from extractNLP import Extract

file = Parse("languages_a5.htm")
file_lang_5 = file.getContent()
# {'wordNE': {u'Brown': u'PERSON', u'Okrand': u'PERSON', u'Marc': u'PERSON', u'daily': u'SET', u'CBS': u'ORGANIZATION', u'3000': u'NUMBER', u'Jonathan': u'PERSON', u'first': u'ORDINAL'}, 'rawSentence': u'The language is displayed in both Latin and pIqaD fonts, making this the first language course written in pIqaD and approved by CBS and Marc Okrand.', 'parsedSentence': ['S', ['NP', ['DT', 'The'], ['NN', 'language']], ['VP', ['VBZ', 'is'], ['VP', ['VBN', 'displayed'], ['PP', ['IN', 'in'], ['NP', ['CC', 'both'], ['NP', ['JJ', 'Latin']], ['CC', 'and'], ['NP', ['NN', 'pIqaD'], ['NNS', 'fonts']]]], [','], ['S', ['VP', ['VBG', 'making'], ['S', ['NP', ['DT', 'this']], ['NP', ['NP', ['DT', 'the'], ['JJ', 'first'], ['NN', 'language'], ['NN', 'course']], ['VP', ['VP', ['VBN', 'written'], ['PP', ['IN', 'in'], ['NP', ['NN', 'pIqaD']]]], ['CC', 'and'], ['VP', ['VBN', 'approved'], ['PP', ['IN', 'by'], ['NP', ['NNP', 'CBS'], ['CC', 'and'], ['NNP', 'Marc'], ['NNP', 'Okrand']]]]]]]]]]], ['.']]}


phrase = Extract(file_lang_5)
res = phrase.getText()
# {'NP': ['The language '], 'VP': ['is displayed in both Latin and pIqaD fonts  making  this  the first language course  written in pIqaD and approved by CBS and Marc Okrand '], '.': ['']}