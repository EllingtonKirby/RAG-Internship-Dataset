import re
import Stemmer
import math
import sqlite3
import json 
from collections import defaultdict 

def create_inverted_index():
  con = sqlite3.connect("internships.db")
  all_internships = con.cursor().execute("SELECT * FROM internship").fetchall()
  con.commit()
  num_internships = len(all_internships)

  # Map
  stop_words=set()
  with open("stop_words.txt") as f:
      for line in f:
          stop_words.add(line.rstrip('\r\n'))

  en_stemmer = Stemmer.Stemmer('english')
  fr_stemmer = Stemmer.Stemmer('french')
  mapped = []
  for title, organization, supervisor, description, _ in all_internships:
      key = title
      value = f"{title} {organization} {supervisor} {description}"
      it = re.finditer(r"\w+", value, re.UNICODE)
      words = defaultdict(int)
      length = 0
      for match in it:
          token = match.group().lower()
          if not(token in stop_words):
              length = length+1
              token_en = en_stemmer.stemWord(token)
              token_fr = fr_stemmer.stemWord(token)
              words[token_en] = words[token_en] + 1
              words[token_fr] = words[token_fr] + 1
      for word, count in words.items():
          mapped.append((word, key, count*1./length))

  # Shuffle
  shuffled = defaultdict(list)
  for (word, title, count) in mapped:
     shuffled[word].append((title, count))

  # Reduce
  inverted_index = dict()
  for key, values in shuffled.items():
    idf = math.log(num_internships*1./len(values))
    result = []
    for value in values:
        document, count = value[0], value[1]
        count = float(count)
        count *= idf
        result.append([document, count])
    result.sort(key=lambda x: x[1], reverse=True)
    inverted_index[key] = result
  
  return inverted_index

if __name__=='__main__':
  index = create_inverted_index()
  with open('internship_search_index', 'w') as output: 
     output.write(json.dumps(index))

  print('Testing the index: searching for "psl"')
  print(index['psl'])
  


