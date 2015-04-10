from parseNLPfinal import *
file = Parse("languages_a9.htm")
a = file.getContent()
b = Extract(a)
b.getPhrases()


