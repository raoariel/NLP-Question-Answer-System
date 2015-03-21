import sqlite3 as lite
con = None
con = lite.connect('test.db')

cur = con.cursor()
cur.execute('SELECT SQLITE_VERSION()')

try: 
  cur.execute('''DROP TABLE relationsParent''')
  print("Resetting parent table.")
except: 
  print("No pre-existing parent table.")
  pass

try: 
  cur.execute('''DROP TABLE relationsChild''')
  print("Resetting child table.")
except: 
  print("No pre-existing child table.")
  pass

cur.execute('''CREATE TABLE relationsParent
               (id integer, NER text, count integer)''')
cur.execute('''CREATE TABLE relationsChild
               (id integer, parent_id integer, relation text)''')


# SELECT * FROM relationsChild WHERE parent_id = 1 






