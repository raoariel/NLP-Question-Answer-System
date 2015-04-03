# Load in dependancies
import os, sys, re, string, ast, json
from  nltk import *
from corenlp import *
from random import randint
from bs4 import BeautifulSoup
from collections import Counter

debug = False
# non deterministically find important content

class Parse(object):
    # textRange 15
    def __init__(self,fileName,dataDir='../sampleData/languages/',textRange=5,ignoreUnicode=True):
        """Parse(fileName,dataDir='../NLP-Question-Answer-System/sampleData/languages/',textRange=5)"""
        self.fileName = fileName
        self.dataDir = dataDir
        self.textRange = textRange+1 # lines of text to search over, +1 for range offset
        self.ignoreUnicode = ignoreUnicode
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
        try:
          html = BeautifulSoup(open(self.dataDir+self.fileName))
          self.raw = html.get_text()
        except:
          raise Exception("Could not read file. Check that the file name and directory are correct. " +
                          "The file extension should be .htm.")
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
                ind += 1
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
        topicNE = None
        
        while ((not lineFound) and (attempts < 5)):
            while (topicNE == None):
                try:
                    topicNE = mostCommonNE[randint(0,max(topNE-1,1))]
                except: pass
            #print topicNE
            #print "here"
            self.getTopicSentence(topicNE)
            #print "not here"
            try:
                parseTree = self.parsedText[self.topicInd]['sentences'][0]['parsetree']
                rawSentence = self.parsedText[self.topicInd]['sentences'][0]['text']
            except:
                raise Exception ("Invalid parse. Could not decode results.")
            #print "at A"
            self.parseTree = self.treeToList(parseTree)
            selectedPhrase = self.parseTree[1] # ROOT extracted
            # try:
            #     if selectedPhrase[0] == 'FRAG':
            #         print("This is a fragment. Ignoring...")
            #         self.getContent()    
            # except: pass

            #print "at B"
            #print selectedPhrase
            #print rawSentence
            if len(rawSentence.split()) > 6:
                lineFound = True
            attempts += 1
        if (attempts > 5):
            print "Timeout finding line with good content. Trying new block..."
            self.getContent()
        #print rawSentence
        if ((unicode("&#") in rawSentence) and self.ignoreUnicode):
            print "Sentence had non-ascii. Ignoring..."
            self.getContent()    
        self.result = (selectedPhrase,rawSentence)  

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
        self.selectLine()
        return self.result
