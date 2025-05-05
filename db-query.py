import sqlite3

conn = sqlite3.connect('hw13.db')
c = conn.cursor()

c.execute('''Select * From students''' )

print('student_info')
conn.commit()
conn.close()
