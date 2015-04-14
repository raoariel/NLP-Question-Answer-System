import sys
import numpy
from corenlp import *
import nltk
import nltk.data
import collections
import yesno
import json
from bs4 import BeautifulSoup



# Setup
corenlp = StanfordCoreNLP()
sent_detector = nltk.data.load("tokenizers/punkt/english.pickle")

# Hardcoded word lists
yesnowords = ["can", "could", "would", "is", "does", "has", "was", "were", "had", "have", "did", "are", "will"]
commonwords = ["the", "a", "an", "is", "are", "were", "."]
questionwords = ["who", "what", "where", "when", "why", "how", "whose", "which", "whom"]

# Take in a tokenized question and return the question type and body
def processquestion(qwords):
    
    # Find "question word" (what, who, where, etc.)
    questionword = ""
    qidx = -1

    for (idx, word) in enumerate(qwords):
        if word.lower() in questionwords:
            questionword = word.lower()
            qidx = idx
            break
        elif word.lower() in yesnowords:
            return ("YESNO", qwords)

    if qidx < 0:
        return ("MISC", qwords)

    if qidx > len(qwords) - 3:
        target = qwords[:qidx]
    else:
        target = qwords[qidx+1:]
    type = "MISC"

    # Determine question type
    if questionword in ["who", "whose", "whom"]:
        type = "PERSON"
    elif questionword == "where":
        type = "PLACE"
    elif questionword == "when":
        type = "TIME"
    elif questionword == "how":
        if target[0] in ["few", "little", "much", "many"]:
            type = "QUANTITY"
            target = target[1:]
        elif target[0] in ["young", "old", "long"]:
            type = "TIME"
            target = target[1:]

    # Trim possible extra helper verb
    if questionword == "which":
        target = target[1:]
    if target[0] in yesnowords:
        target = target[1:]
    
    # Return question data
    return (type, target)

# Get command line arguments
articlefilename = sys.argv[1]
questionsfilename = sys.argv[2]

# Process article file
article = open(articlefilename, 'r')
article = BeautifulSoup(article).get_text()
article = ''.join([i if ord(i) < 128 else ' ' for i in article])
article = article.replace("\n", " . ")
article = sent_detector.tokenize(article)

# Process questions file
questions = open(questionsfilename, 'r').read()
questions = questions.decode('utf-8')
questions = questions.splitlines()

# Iterate through all questions
for question in questions:

    # Answer not yet found
    done = False

    # Tokenize question
    print question
    qwords = nltk.word_tokenize(question.replace('?', ''))
    questionPOS = nltk.pos_tag(qwords)

    # Process question
    (type, target) = processquestion(qwords)

    # Answer yes/no questions
    if type == "YESNO":
        yesno.answeryesno(article, qwords)
        continue

    # Get sentence keywords
    searchwords = set(target).difference(commonwords)
    dict = collections.Counter()
        
    # Find most relevant sentences
    for (i, sent) in enumerate(article):
        sentwords = nltk.word_tokenize(sent)
        wordmatches = set(filter(set(searchwords).__contains__, sentwords))
        dict[sent] = len(wordmatches)
     
    # Focus on 10 most relevant sentences
    for (sentence, matches) in dict.most_common(10):
        parse = json.loads(corenlp.parse(sentence))
        sentencePOS = nltk.pos_tag(nltk.word_tokenize(sentence))

        # Attempt to find matching substrings
        searchstring = ' '.join(target)
        if searchstring in sentence:
            startidx = sentence.index(target[0])
            endidx = sentence.index(target[-1])
            answer = sentence[:startidx]
            done = True
    
        # Check if solution is found
        if done:
            continue

        # Check by question type
        answer = ""
        for worddata in parse["sentences"][0]["words"]:
            
            # Mentioned in the question
            if worddata[0] in searchwords:
                continue
            
            if type == "PERSON":
                if worddata[1]["NamedEntityTag"] == "PERSON":
                    answer = answer + " " + worddata[0]
                    done = True
                elif done:
                    break

            if type == "PLACE":
                if worddata[1]["NamedEntityTag"] == "LOCATION":
                    answer = answer + " " + worddata[0]
                    done = True
                elif done:
                    break

            if type == "QUANTITY":
                if worddata[1]["NamedEntityTag"] == "NUMBER":
                    answer = answer + " " + worddata[0]
                    done = True
                elif done:
                    break

            if type == "TIME":
                if worddata[1]["NamedEntityTag"] == "NUMBER":
                    answer = answer + " " + worddata[0]
                    done = True
                elif done:
                    answer = answer + " " + worddata[0]
                    break
            
    if done:
        print answer

    if not done:
        (answer, matches) = dict.most_common(1)[0]
        print answer
