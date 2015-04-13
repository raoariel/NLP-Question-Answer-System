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
	stringg = stringg.replace(', []', '')
	return ast.literal_eval(stringg)

