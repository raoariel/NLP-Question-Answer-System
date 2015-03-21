# WARNING directories are hard-coded atm
import os, sys, re, string, ast, json, yaml
import convert
from  nltk import *
from corenlp import *
from bs4 import BeautifulSoup
from collections import Counter

debug = 1

dataDir = '../NLP-Question-Answer-System/sampleData/'
htmlFile = sys.argv[1]
html = BeautifulSoup(open(dataDir+htmlFile))
raw = html.get_text()
# print raw

try: 
  misc = raw.index("See also")
  raw = raw[:misc]
except:
  pass

text = tokenize.sent_tokenize(raw)



corenlp = StanfordCoreNLP()
text0 = text[0] # filler for now
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

print convert.treeToList(parseTree)

# Question Gen: 
# use Counter to find most freq Named Entities
# randint to get sentence with it, 
# Parse tree to extract necessary components 















def treeToList (string): 
  ''' Converts parse tree to nested list.
      Source: http://stackoverflow.com/questions/27612254/ '''
  string = string.replace('(', '[')
  string = string.replace(')', ']')
  string = string.replace('] [', '], [')
  string = re.sub(r'(\w+)', r'"\1",', string)
  return ast.literal_eval(string)

