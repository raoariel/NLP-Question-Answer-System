import sys
import numpy
import nltk
import nltk.data
import collections
import yesno

sent_detector = nltk.data.load("tokenizers/punkt/english.pickle")
yesnowords = ["is", "does", "has", "was", "were", "had", "have", "did", "are"]
questionwords = ["who", "what", "where", "when", "why", "how", "whose", "which"]
commonwords = ["the", "a", "an", "is", "are", "were", "."]

# Get names of files to parse
#articlenum = sys.argv[1]
#articlefilename = 'raw_project_data/' + articlenum + '.txt'
#questionsfilename = 'raw_project_data/q' + articlenum + '.txt'

articlefilename = sys.argv[1]
questionsfilename = sys.argv[2]

# Open article file
article = open(articlefilename, 'r').read()
article = article.decode('utf-8')
article = article.replace("\n", " . ")
article = sent_detector.tokenize(article)

# Open questions file
questions = open(questionsfilename, 'r').read()
questions = questions.decode('utf-8')
questions = questions.splitlines()

# Iterate through all questions
for questionstr in questions:
    question = nltk.word_tokenize(questionstr)
    done = False

    # Find "question word" (what, who, where, etc.)
    questionword = ""
    questionrem = []

    for (idx, word) in enumerate(question):
        if word.lower() in questionwords:
            questionword = word.lower()
            qidx = idx
            questionrem = question[idx+1:-1] 
            break
        elif word.lower() in yesnowords:
            yesno.answeryesno(article, question)
            done = True
            break

    if done:
        continue

    # Account for "compound question words"
    if questionword == "which" or questionword == "how":
        questionrem = questionrem[1:]

#    print questionword
 #   print questionrem



    # Get sentence keywords
    searchwords = set(question).difference(commonwords)
    searchwords = set(question).difference(commonwords)
    dict = collections.Counter()

    # Find most relevant sentences
    for (i, sent) in enumerate(article):
        sentwords = nltk.word_tokenize(sent)
        wordmatches = set(filter(set(searchwords).__contains__, sentwords))
        dict[sent] = len(wordmatches)
     
    for (sentence, matches) in dict.most_common(10):
        answer = ' '.join(questionrem)
        #print sentence
        #print answer
        questionPOS = nltk.pos_tag(nltk.word_tokenize(sentence))
    
    done = False
    #print questionPOS
    for (w, pos) in questionPOS:
        if questionword == "who" and pos == "NNP" and not w in searchwords:
            print w
            done = True
            break

        if questionword == "what" and pos == "NNP" and not w in searchwords:
            print w
            done = True
            break
        
        if questionword == "when" and pos == "CD" and not w in searchwords:
            print w
            done = True
            break

        if questionword == "where" and pos == "NNP" and not w in searchwords:
            print w
            done = True
            break
    
    if not done:
        print "?"

#print dict
#print article
