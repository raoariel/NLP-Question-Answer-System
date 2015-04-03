import os, sys, re, string, ast, json, yaml
import convert
from  nltk import *
from corenlp import *
from bs4 import BeautifulSoup
from collections import Counter

debug = False

dataDir = '../NLP-Question-Answer-System/sampleData/'
htmlFile = sys.argv[1]
html = BeautifulSoup(open(dataDir+htmlFile))
raw = html.get_text()
# print raw

## WRITE ACTUAL MODULE ie Parse.extractPhrase(n), Parse.getTree(raw string) etc.

try: 
  misc = raw.index("See also")
  raw = raw[:misc]
except:
  pass

text = tokenize.sent_tokenize(raw)



corenlp = StanfordCoreNLP()
for i in range(10):
  text0 = text[i] # filler for now
  if debug: print text0

  # NTS use json to work with unicode to match raw text
  parse = yaml.load(corenlp.parse(text0))
  if debug: print parse

  try: 
    coref = parse['coref'] # see testCoreNLP.py script
  except:
    if debug: print "No unresolved pronouns."
    coref = None 
    pass

  parseTree = parse['sentences'][0]['parsetree'] ### 
  originalText = parse['sentences'][0]['text']
  dependencies = parse['sentences'][0]['dependencies']
  words = parse['sentences'][0]['words']
  #print (' ')
  #print (originalText)
  #print(parseTree)
  a = convert.treeToList(parseTree)
  #print a

  print (' ')
  print (' ')
  print (' ')
  print (' ')
  while (type(a[1]) == list) and (a[1][0] != 'NP'):
    a = a[1]
  try:
    print(a[1])
    print (' ')
    print (a[2])
    print (' ')
  except:
    print (' ')
  print (' ')
  print (' ')
  
# Question Gen: 
# use Counter to find most freq Named Entities
# randint to get sentence with it, 
# Parse tree to extract necessary components 









