import os, sys, re, string, ast, json
from  nltk import *
from corenlp import *
from random import randint
from random import choice
from bs4 import BeautifulSoup
from collections import Counter

class Extract(object):
  def __init__(self,parse):
    """Extracts all sub phrase strings from list at the given level is the parse tree.
    If no phrase exists, will return None type."""
    try: 
      self.parseList = parse["parse"]
      self.raw = parse["raw"]
    except: 
      self.parseList = []
      self.raw = ""
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
    if ((self.parseList == []) or (self.raw == "")): return None
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

