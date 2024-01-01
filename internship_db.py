import sqlite3
import json
import re
from argparse import ArgumentParser

def create_interships_table():
  con = sqlite3.connect("internships.db")
  cur = con.cursor()
  cur.execute("CREATE TABLE internship(title TEXT UNIQUE,\
               organization TEXT, \
              supervisor TEXT, \
              description TEXT, \
              source TEXT,\
              PRIMARY KEY (title,organization))")
  con.commit()

def insert_json_source(json_file, source):
  con = sqlite3.connect("internships.db")
  cur = con.cursor()
  with open(json_file, encoding="utf8") as f:
    data = json.load(f)
    transaction = [
      (item['title'], item['organization'], item['supervisor'], item['description'], source) for item in data
    ]
    cur.executemany("INSERT OR IGNORE INTO internship VALUES(?, ?, ?, ?, ?)", transaction)
    con.commit()

def test_internships_db():
  con = sqlite3.connect("internships.db")
  cur = con.cursor()
  for row in cur.execute("SELECT * FROM internship"):
    print(row)
  print("Internships Test Success")

def assess_quality():
  conn = sqlite3.connect('internships.db')
  cursor = conn.cursor()

  # 1. Duplicates
  print("\nDuplicates ")
  query_duplicates_title = f"SELECT title,organization, COUNT(*) FROM internship GROUP BY\
      title,organization HAVING COUNT(*) > 1;"
  cursor.execute(query_duplicates_title)
  duplicates_title = cursor.fetchall()

  if duplicates_title:
      print("\tDuplicates for (title, organization):")
      for duplicate in duplicates_title:
          print(f"\t Title: {duplicate[0]}, Organization: {duplicate[1]}, Nb: {duplicate[2]}")
  else:
      print("\tNo duplicates")
  print('-'*100)   

  # 2. NULL values
  print("NULL value ")
  to_assess = ['title', 'organization', 'supervisor', 'description', 'source']
  for column in to_assess:
      query = f"SELECT COUNT(*) FROM internship WHERE {column} IS NULL;"
      cursor.execute(query)
      count_null = cursor.fetchone()[0]
      print(f"\tNumber of NULL values in '{column}': {count_null}")
  print('-'*100)

  # 3. Sources diversity
  query_unique_sources = f"SELECT source, count(*) FROM internship GROUP by source;"
  cursor.execute(query_unique_sources)
  unique_sources = cursor.fetchall()
  print("Sources diversity:")
  for source in unique_sources:
      print('\t' + str(source[0])+' '+ str(source[1]))
  print('-'*100)

  # 4. Description length analysis in terms of words
  print(f"Descriptions lentgh analysis")
  query_description_stats = f"""
    SELECT
        MIN(LENGTH(description) - LENGTH(REPLACE(description, ' ', ''))) + 1 AS min_length_words,
        AVG(LENGTH(description) - LENGTH(REPLACE(description, ' ', ''))) + 1 AS avg_length_words,
        MAX(LENGTH(description) - LENGTH(REPLACE(description, ' ', ''))) + 1 AS max_length_words
    FROM internship;
"""
  
  cursor.execute(query_description_stats)
  description_stats = cursor.fetchone()
  min_length_words = description_stats[0]
  avg_length_words = description_stats[1]
  max_length_words = description_stats[2]
  print(f"\tMinimum number of words: {min_length_words} words")
  print(f"\tAverage number of words: {avg_length_words:.2f} words")
  print(f"\tMaximum number of words: {max_length_words} words")
  

  conn.close()
  pass

if __name__=='__main__':
  parser = ArgumentParser()
  parser.add_argument("-c", "--create", help="create the internships table", default=None, action='store_true')
  parser.add_argument("-f", "--file", help="filename which contains json to insert to table", default=None)
  parser.add_argument("-t", "--test", help="test the db", default=None, action='store_true')
  parser.add_argument("-a", "--assess", help="assess the quality of the db", default=None, action='store_true')
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
  if args.assess != None:
    assess_quality()
