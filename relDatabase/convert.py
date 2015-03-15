import re, ast, string

def treeToList (string):
  ''' Converts parse tree to nested list.
      Source: http://stackoverflow.com/questions/27612254/ '''
  string = string.replace('(', '[')
  string = string.replace(')', ']')
  string = string.replace('] [', '], [')
  string = re.sub(r'(\w+)', r'"\1",', string)
  return ast.literal_eval(string)



