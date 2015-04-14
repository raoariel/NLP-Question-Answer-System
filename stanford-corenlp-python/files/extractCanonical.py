import os, sys, re, string, ast, json
from  nltk import *
from corenlp import *
from random import randint
from random import choice
from bs4 import BeautifulSoup
from collections import Counter

# Return largest NP VP pair for the given sentence

class ExtractCanonical(object):
	def __init__(self,parse,level=1):
		"""Extracts largest phrase strings from list at the given level 
		   is the parse tree. 
		   If no phrase exists, will return None type."""
		try:
			self.parseList = parse["parse"]
	      	self.raw = parse["raw"]
	    except:
	    	self.parseList = []
	      	self.raw = ""
		return 

	def getString(self,subParse,acc): 
		if (subParse == []): return ""
		elif all((type(x) == str) for x in subParse): 
			try:
				return (subParse[1] + " ")
			except:
				pass
		for tok in subParse:
			if (type(tok) == list):
				acc += self.getString(tok," ")
		return acc

		
	def getText(self):
		"""Returns dictionay of (POS,phrase) kv pairs."""
		# Removes 'S' tag and [] end of line
		if ((self.parseList == []) or (self.raw == "")): return None
		self.results = dict()
		innerList = []
		sub = []
		for stree in self.parseList[1:]:
			try:
				if (stree[0] == 'S'):
					innerList += stree[1:]
				else:
					innerList.append(stree)
			except:
				pass
		for sub in innerList:
			if (sub == []): pass 
			else:
				pos = sub[0]
				string = self.getString(sub[1:],"")
				string = string.replace('  ', ' ')
				try:
					if string[0] == " ": 
						string = string[1:]
				except: pass
				try:
					tmp = self.results[pos]
					rself.esults[pos] = tmp.append(string)
				except:
					self.results[pos] = [string]
				for i in sub[1:]:
					if (type(i) == list):
						for j in i:
							if "VP" in j:
								sub_vp = self.getString(j,"")
								sub.append(sub_vp)
		return self.results


	def tag(s):
		import nltk
		text = nltk.word_tokenize(s)
		return nltk.pos_tag(text)

	def supersense(entity):
		import os
		return map(lambda y: y.split("\t"), 
		os.popen("cd SupersenseTagger && ./run.sh <<< \"" + entity+ "\" cd ..").read().split("\n"))

	def get_questions(self):
		z = self.getText()
		(subj,vp) = (z['NP'][0], z['VP'][0])
                from pattern.en import lexeme, lemma, tenses
		import nltk, re
		tagged = nltk.pos_tag(nltk.word_tokenize(subj + " " + vp))
                verb = ""
		sense = supersense(subj)
		if(sense[0][2][-6:] == 'person' or sense[0][1] == 'PRP'): return ("Who " + vp + "?")
		elif(sense[0][2][-4:] == 'time' or re.match("[1|2]\d\d\d", subj)): return ("When " + vp + "?")
		elif(sense[0][2][-8:] == 'location' and
		('PP' in z and z['PP'].split()[0].lower in ["on", "in", "at", "over", "to"])):
			return ("Where " + vp + "?")
                aux = ["Will","Shall","May","Might","Can","Could","Must","Should","Would","Do","Does","Did"]
                for i in reversed(tagged):
                        if(i[1][0] == 'V'):
                                verb = i[0]
                if((u'' + verb) in lexeme("is")):
                        return (verb.capitalize() + " " + subj.lower() + vp[len(verb):] + "?")
                else:
                        for x in aux:
                                if(tenses(x)[0] == tenses(verb)[0]):
                                        return (x + " " + subj.lower() + " " + lemma(verb) + vp[len(verb):] + "?")

