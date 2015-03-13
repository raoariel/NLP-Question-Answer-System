import sqlite3 as lite
con = None
con = lite.connect('test1.db')

cur = con.cursor()
cur.execute('SELECT SQLITE_VERSION()')

try: cur.execute('''DROP TABLE relations''')
except: pass

cur.execute('''CREATE TABLE relations 
		(NER text, relation text, count integer)''')

val = ('president','of the US', 1)
cur.execute('INSERT INTO relations VALUES (?,?,?)', val) 
val2 = ('presidental candidate','of the US', 2)
cur.execute('INSERT INTO relations VALUES (?,?,?)', val2) 

countedMax = []
for row in cur.execute('SELECT * FROM relations ORDER BY count DESC'):
  print row
  countedMax.append(row)

#countedMax = []
#cur.execute("Select Max(count) from relations")
#for row in cur.fetchall():
#  countedMax.append(row)




print countedMax
con.close()




