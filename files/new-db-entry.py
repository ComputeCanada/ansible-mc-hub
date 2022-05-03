#!/usr/bin/env python3
import sqlite3
from json import dumps

import yaml

def main(filename):
  with open(filename, 'r') as file:
    user_project_map = yaml.safe_load(file)

  with sqlite3.connect('database.db') as con:
    cur = con.cursor()
    cur.execute("DELETE FROM users")
    statement = """
    INSERT INTO users (username, projects) VALUES (?, ?)
    """

    for (username, projects) in user_project_map.items():
      cur.execute(statement, (username, dumps(projects)))

    con.commit()

if __name__ == "__main__":
  import sys
  if len(sys.argv) > 1:
    main(sys.argv[1])
