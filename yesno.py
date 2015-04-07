import sys
import nltk.data
import nltk

def answeryesno(article, question):
    questionstr = ' '.join(question)
    questionstr = questionstr.lower()
    question = nltk.pos_tag(question)
    answer = "no"
    keyword = ""
    for (word,pos) in question:
        if (pos == 'NN' or pos == 'NNS' or pos == 'NNP' or pos == 'NNPS'):
            keyword = word.lower()
            answer = "no"
    for sentence in article:
       # print sentence
        if answer == "yes":
            break
        s = nltk.word_tokenize(sentence.lower())
        if keyword in s:
            #print sentence
            answer = "yes"
            for (word,pos) in question:
                if answer == 'no': 
                    break
                if (pos != '.') and (word.lower() not in s) and (pos != 'DT') and (word != 'does') and (word != 'do'):
                    answer = 'no'                    
                    if pos[0] == 'V':
                        tempword = nltk.stem.wordnet.WordNetLemmatizer().lemmatize(word,'v')                       
                        for (w,p) in nltk.pos_tag(s):
                            if p[0] == 'V':
                                if tempword == nltk.stem.wordnet.WordNetLemmatizer().lemmatize(w,'v'):
                                    answer = 'yes'
                    elif word in article[0]:                       
                        answer = "yes" 

    #print questionstr,answer
    print answer
