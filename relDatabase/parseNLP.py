# Load in dependancies
import os, sys, re, string, ast, json, yaml
from  nltk import *
from corenlp import *
from random import randint
from bs4 import BeautifulSoup
from collections import Counter

debug = False
# non deterministically find important content

class Parse(object):
    # textRange 15
    def __init__(self,fileName,dataDir='../NLP-Question-Answer-System/sampleData/',textRange=5):
        """Parse(fileName,dataDir='../NLP-Question-Answer-System/sampleData/',textRange=5)"""
        self.fileName = fileName
        self.dataDir = dataDir
        self.textRange = textRange+1 # lines of text to search over, +1 for range offset
        print("Reading file..."),
        self.readFile()
        print("OK!")
        print("Tokenizing file..."),
        self.tokenize()
        print("OK!")
        print("Starting StanfordCoreNLP..."),
        self.corenlp = StanfordCoreNLP()
        print("OK!")
        return

    def readFile(self):
        """Load in html file and extract raw text."""
        html = BeautifulSoup(open(self.dataDir+self.fileName))
        self.raw = html.get_text()
        return 

    def tokenize(self):
        """Tokenize raw text to prepare for parsing."""
        try: 
          misc = self.raw.index("See also")
          self.raw = self.raw[:misc]
        except:
          pass
        self.text = tokenize.sent_tokenize(self.raw)
        self.textLen = len(self.text)
        return

    def getNECounts(self,line):
        """Collect and store counts of named entities within the sentence."""
        try:
            sentence = line[0]['words']
            for token in sentence:
                word = token[0]
                info = token[1]
                if info['NamedEntityTag'] != 'O':
                    self.NEcounts[word] += 1
        except:
            raise Exception ("Failed coreNLP parse. \n Text: ", line)
        return

    def getTopicSentence(self,topicNE):
        """Select a sentence with a given named entity."""
        self.topicInd = -1 #get sentence with topic in it
        ind = 0
        while (self.topicInd < 0):
            try:
                tmp = self.parsedText[ind]['sentences'][0]['text']
                if topicNE in tmp:
                   self.topicInd = ind
                else: ind += 1
            except:
                pass
        return

    def treeToList(self,parseTree):
        """Convert parse tree from string to nested array"""
        validChar = string.ascii_letters + string.digits + "() "
        filterChars = (lambda x: ((x not in string.punctuation) or
                                  (x not in string.punctuation) or 
                                  (x in "() ")))
        parseTree = ''.join(filter(filterChars, parseTree))
        parseTree = parseTree.replace('(', '[')
        parseTree = parseTree.replace(')', ']')
        parseTree = parseTree.replace('] [', '], [')
        parseTree = parseTree.replace('[]', '')
        parseTree = re.sub(r'(\w+)', r'"\1",', parseTree)
        return ast.literal_eval(parseTree)
    
    def selectLine(self):
        (lineFound,attempts) = (False,0)
        uniqueNE = len(list(self.NEcounts))
        topNE = uniqueNE // 4
        mostCommonNE = [k for (k,v) in self.NEcounts.most_common(topNE)]
        
        while ((not lineFound) and (attempts < 5)):
            topicNE = mostCommonNE[randint(0,topNE-1)]
            print topicNE
            self.getTopicSentence(topicNE)
            try:
                parseTree = self.parsedText[self.topicInd]['sentences'][0]['parsetree']
                rawSentence = self.parsedText[self.topicInd]['sentences'][0]['text']
            except:
                raise Exception ("Invalid parse. Could not decode results.")
            self.parseTree = self.treeToList(parseTree)
            selectedPhrase = self.parseTree[1] # ROOT extracted
            #print selectedPhrase
            #print rawSentence
            if len(rawSentence.split()) > 6:
                lineFound = True
            attempts += 1
        if (attempts > 5):
            print "Timeout finding line with good content. Trying new block..."
            self.getContent()
        return (selectedPhrase,rawSentence)

    def decomposePhrase(self):
        """Use parse tree to extract noun phrase and verb phrase."""
        while (type(phrase) == list) and (phase[1][0] != 'NP'):
                phrase = phrase[1]
        print(phrase[1],phrase[3])
        #FINISH LATER IF NEEDED
        return

    def getContent(self):
        """Return sentence and corresponding parse tree with important content."""
        # Assumption: python PRNG goodish
        #             there is some worthwhile content every 15 sentences
        startInd = randint(0,self.textLen-self.textRange)
        self.parsedText = []
        self.NEcounts = Counter()
        print ("Parsing lines: "),
        for lineInd in xrange(startInd,startInd+self.textRange):
            print lineInd,
            line = self.text[lineInd]
            if isinstance(line, unicode):
                strLine = line.encode('ascii', 'xmlcharrefreplace')
                try: 
                    res = json.loads(self.corenlp.parse(strLine))
                    self.parsedText.append(res)
                    self.getNECounts(res['sentences'])
                except: pass
            else: raise Exception ("Invalid encoding for text file.")

        print "Block Complete."
        # #(phraseNP,phraseVP) = self.decomposePhrase()
        # #return raw line with parse, NP pharse, VP phrase
        # #return (phrase,rawSentence,phraseNP,phraseVP)
            
        #return (selectedPhrase,rawSentence)
        return self.selectLine()


