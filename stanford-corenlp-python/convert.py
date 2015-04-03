import re, ast, string

def treeToList (stringg):
	validChar = string.ascii_letters + string.digits + "() "
	all = string.maketrans('','')
	removeInvalidChar = all.translate(all, validChar)
	stringg = stringg.translate(all, removeInvalidChar)

	stringg = stringg.replace('(', '[')
	stringg = stringg.replace(')', ']')
	stringg = stringg.replace('] [', '], [')
	stringg = stringg.replace('[]', '')
	stringg = re.sub(r'(\w+)', r'"\1",', stringg)
	return ast.literal_eval(stringg)


def treeToList23 (stringg):
	validChar = string.ascii_letters + string.digits + "()"
	for a in stringg:
		if a not in validChar:
			stringg = stringg.replace(a, '')
	stringg = stringg.replace('(', '[')
	stringg = stringg.replace(')', ']')
	stringg = stringg.replace('] [', '], [')
	stringg = re.sub(r'(\w+)', r'"\1",', stringg)
	return ast.literal_eval(string)

def treeToList2 (string):
  ''' Converts parse tree to nested list.
      Source: http://stackoverflow.com/questions/27612254/ '''
  string = string.replace('(', '[')
  string = string.replace(')', ']')
  string = string.replace('] [', '], [')
  string = string.replace('. .', '"."')
  string = re.sub(r'(\w+)', r'"\1",', string)
  #return eval(string)
  return ast.literal_eval(string)



