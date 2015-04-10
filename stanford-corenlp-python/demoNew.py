from parseNLPNew import *
file = Parse("languages_a9.htm")
a = file.getContent()
b = Extract(a)
b.getPhrases()


## todo since there are NP in VP's maybe just pick an NP that is not a subset of the vp...
# or filter them out..
# mehh idk