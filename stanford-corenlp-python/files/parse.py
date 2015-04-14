import os, sys, re, string, ast, json
from  nltk import *
from corenlp import *
from random import randint
from random import choice
from bs4 import BeautifulSoup
from collections import Counter

class Parse(object):
  def __init__(self,fileName,dataDir='../sampleData/languages/'):
    self.fileName = fileName
    self.dataDir = dataDir
    self.readFile()
    self.tokenize()
    self.corenlp = StanfordCoreNLP()
    self.getMain()
    self.rem = []
    self.parseList = []
    self.line = ""
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

  def getLine(self):
    found = False
    if self.topic == None: pass 
    while not found:
      if self.text == []:
        self.line = self.rem[0]
        self.rem = self.rem[1:]
        return
      r = randint(0,max(0,len(self.text)-1))
      self.line = self.text[r]
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
