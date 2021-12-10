import sqlite3
from json import dumps

con = sqlite3.connect('database.db')
cur = con.cursor()
usernames = [
    'fafor10@computecanada.ca',
    'dboss@computecanada.ca',
    'jralbert@computecanada.ca',
    'jfaure@computecanada.ca'
]
projects = [
    'arbutus:training',
    'beluga:training'
]

statement = """
INSERT INTO users (username, projects) VALUES (?, ?)
"""

for username in usernames:
  cur.execute(statement, (username, dumps(projects)))

con.commit()
con.close()
