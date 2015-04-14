import os, sys, re, string, ast, json
from  nltk import *
from corenlp import *
from random import randint
from random import choice
from bs4 import BeautifulSoup
from collections import Counter
# fall back for if so many question self.text = []
# have another loop guard for while not found


# maybe add condition for pronoun????
class Parse(object):
  def __init__(self,fileName,dataDir='../sampleData/languages/'):
    self.fileName = fileName
    self.dataDir = dataDir
    self.readFile()
    self.tokenize()
    self.corenlp = StanfordCoreNLP()
    self.getMain()
    self.rem = []
    return

  def readFile(self):
    html = BeautifulSoup(open(self.dataDir+self.fileName))
    self.raw = html.get_text()
    return 

  def tokenize(self):
    try: 
      misc = self.raw.index("See also")
      self.raw = self.raw[:misc]
    except:
      pass
    self.text = tokenize.sent_tokenize(self.raw)
    self.textLen = len(self.text)
    return

  def getMain(self):
    main = self.text[0]
    self.topic = Counter(main.split()).most_common(1)[0][0]
    return

  def getMain2(self):
    main = self.text[0]
    #self.text = self.text[1:]
    term = re.match(r'\n\n\n(.*)\n\n\n\n',main)
    try: 
      self.topic = term.group(1)
    except: 
      self.topic = None
    return 

  def getLine(self):
    found = False
    if self.topic == None: pass # format assumption failed, need backup :(
    while not found:
      if self.text == []:
        self.line = self.rem[0]
        self.rem = self.rem[1:]
        return
      r = randint(0,max(0,len(self.text)-1))
      self.line = self.text[r]
      # arbitrary semi-educated conditions :D
      if (self.topic in self.line):
        if (len(self.line) > 80):
          if ('\n' not in self.line):
            found = True
      self.text.remove(self.line)
      self.rem.append(self.line)
    return 

  def treeToList(self):
    invalidChar = u'!"#%\'*+,-./:;<=>?@[\]^_`{|}~'
    translateTo = u''
    translateTable = dict((ord(char), translateTo) for char in invalidChar)
    self.parse = self.parse.translate(translateTable)
    self.parse = self.parse.replace('(', '[')
    self.parse = self.parse.replace(')', ']')
    self.parse = self.parse.replace('] [', '], [')
    self.parse = re.sub(r'(\w+)', r'"\1",', self.parse)
    self.parse = self.parse.replace(',]', ']')
    self.parse = self.parse.replace(', [ ]', '')
    try:
      return ast.literal_eval(self.parse)
    except:
      return []

  def getContent(self):
    self.getLine()
    try: 
      self.coreParse = json.loads(self.corenlp.parse(self.line))
      self.parse = self.coreParse['sentences'][0]['parsetree']
    except: 
      return self.getContent
    self.parseList = self.treeToList()
    if self.parseList == []:
      return self.getContent
    return {"parse":self.parseList, "raw":self.line}
    

class Extract(object):
  def __init__(self,parse):
    """Extracts phrase strings from list at the given level is the parse tree. If provided level is invalid, will return phrases of highest order.
    If no phrase exists, will return None type."""
    try: 
      self.parseList = parse["parse"]
      self.raw = parse["raw"]
    except: 
      pass
    return 

  def getAllSub(self,l):
    a = []
    for sub in l:
      if type(sub) == list:
        a.append(sub)
        a += self.getAllSub(sub)
    return a

  def filterSub(self,l):
    goodSub = []
    for sub in l:
      if ('NP' in sub) or ('VP' in sub):
        goodSub.append(sub)
    return goodSub

  def getString(self,l):
    s = ''
    try:
      if type(l[1]) == list:
        for x in l[1:]:
          s += self.getString(x)
      else:
        if l[0] != l[1]:
          s += l[1] + " "
    except: pass
    return s

  def getPhrases(self):
    allSub = self.getAllSub(self.parseList)
    goodSub = self.filterSub(allSub)
    res = dict()
    for sub in goodSub:
      pos = sub[0]
      phrase = self.getString(sub)
      if pos in res:
        res[pos].append(phrase)
      else:
        res[pos] = [phrase]
    for key in res:
      res[key].sort(key = lambda s: len(s))
    return res

