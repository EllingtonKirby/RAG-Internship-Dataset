import sqlite3
import json
import re
from argparse import ArgumentParser

def create_interships_table():
  con = sqlite3.connect("internships.db")
  cur = con.cursor()
  cur.execute("CREATE TABLE internship(title, organization, supervisor, description, source)")
  con.commit()

def insert_json_source(json_file, source):
  con = sqlite3.connect("internships.db")
  cur = con.cursor()
  with open(json_file, encoding="utf8") as f:
    data = json.load(f)
    transaction = [
      (item['title'], item['organization'], item['supervisor'], item['description'], source) for item in data
    ]
    cur.executemany("INSERT INTO internship VALUES(?, ?, ?, ?, ?)", transaction)
    con.commit()

def test_internships_db():
  con = sqlite3.connect("internships.db")
  cur = con.cursor()
  for row in cur.execute("SELECT * FROM internship"):
    print(row)
  print("Internships Test Success")

if __name__=='__main__':
  parser = ArgumentParser()
  parser.add_argument("-c", "--create", help="create the internships table", default=None, action='store_true')
  parser.add_argument("-f", "--file", help="filename which contains json to insert to table", default=None)
  parser.add_argument("-t", "--test", help="test the db", default=None, action='store_true')
  args = parser.parse_args()
  
  if args.create != None:
    create_interships_table()
  if args.file != None:
    result = re.match(r'^(.*)\.[^.]+$', args.file)
    if result:
      source = result.group(1)
      print(f"Reading from source: {source}")
      insert_json_source(args.file, source=source)
    else:
      print("No source found.")
  if args.test != None:
    test_internships_db()
