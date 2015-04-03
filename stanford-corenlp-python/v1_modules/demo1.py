# Note to self: MUST deal with non-ascii; too limiting in content and time consuming to restart search each time
# Note to self: CAN find way to clean up raw input and optimize for given htmls
#              currently removing index but should also remove charts, examples, etc.




# Demo for parse & extract modules
# Dependencies: 
#   convert.py  parseNLP.py  extractNLP.py
#   os, sys, re, string, ast, json 
#   nltk, corenlp, random, bs4, collections

from parseNLP import Parse
from extractNLP import Extract

file = Parse("languages_a1.htm")

parsed = file.getContent()
word = "hello"
parsed.wordNE[word] # returns Named Entity of 'hello'
# tuple of parse tree as list and raw string
# Example:
# (['S', ['NP', ['DT', 'The'], ['NN', 'palace']], ['VP', ['VBD', 'was'], ['NP', ['NP', ['DT', 'an'], ['NN', 'act']], ['PP', ['IN', 'of'], ['NP', ['NN', 'charity']]]], ['PP', ['IN', 'by'], ['NP', ['NP', ['DT', 'the'], ['NNP', 'Sultan']], ['SBAR', ['WHNP', ['WP', 'who']], ['S', ['VP', ['VBD', 'wanted'], ['S', ['VP', ['TO', 'to'], ['VP', ['VB', 'help'], ['NP', ['DT', 'the'], ['JJ', 'poor']], ['PP', ['IN', 'in'], ['NP', ['NP', ['DT', 'the'], ['JJ', 'neighbouring'], ['NNS', 'areas']], ['PP', ['IN', 'of'], ['NP', ['NNP', 'Pune']]], [], ['SBAR', ['WHNP', ['WP', 'who']], ['S', ['VP', ['VBD', 'were'], ['ADVP', ['RB', 'drastically']], ['VP', ['VBN', 'hit'], ['PP', ['IN', 'by'], ['NP', ['NN', 'famine']]]]]]]]]]]]]]]]]], []], u'The palace was an act of charity by the Sultan who wanted to help the poor in the neighbouring areas of Pune, who were drastically hit by famine.')

phrases = Extract(parsed)

phraseDict = phrases.getText()   
# dictionary with (key: POS tag, value: raw string associated)
# Example: 
# {'NP': ['The palace '], 'VP': ['was  an act of charity by  the Sultan  who  wanted  to help the poor in  the neighbouring areas of Pune  who  were drastically hit by famine ']}
# NOTE: OUTPUT MAY BE NONE: INPUT IS A FRAGMENT NOT SENTENCE: NEED TO GET NEW SENTENCE
# I should handle it for you but check in case...
