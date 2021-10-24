#!/usr/bin/env python3
import sys
import csv
import json
from qwikidata.sparql import return_sparql_query_results

q = """
select ?person ?personLabel ?position ?positionLabel ?nationality ?nationalityLabel (year(?birthDate) as ?birth) (year(?deathDate) as ?death) (year(?positionStart) as ?start) (year(?positionEnd) as ?end) where {
# занимаемая должность
  ?person p:P39 ?positionHeld.
  ?positionHeld ps:P39 ?position.
# год начала занятия позиции
  ?positionHeld pq:P580 ?positionStart.
# год конца занятия позиции
  ?positionHeld pq:P582 ?positionEnd.
# должность - субкласс правителя (wd:Q1097498) или может быть монарха (wd:Q116) или даже суверена (wd:Q2304859)
  ?position wdt:P279* wd:Q2304859.
# Папа Римский формально субкласс монарха, исключим его
  FILTER NOT EXISTS { ?position wdt:P279* wd:Q19546. }
# дата рождения
  ?person wdt:P569 ?birthDate.
# дата смерти
  ?person wdt:P570 ?deathDate.
# деятельность - правитель (плохое свойство, оно мало у кого заполнено, поэтому не используем)
#  ?person wdt:P106 wd:Q1097498
# национальность
  OPTIONAL {
    ?person wdt:P27 ?nationality.
  }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "ru,en". }
}
"""

r = return_sparql_query_results(q)

f = open("data.csv","w")
out = csv.writer(f, quotechar='"', delimiter=',')

out.writerow(["qid","person","position","nationality","birth","start","end","death"])

for row in r["results"]["bindings"]:
  qid = row["person"]["value"].split('/')[-1]
  person = row["personLabel"]["value"]
  position = row["positionLabel"]["value"]
  try:
    birth = row["birth"]["value"]
  except KeyError:
    continue
    birth = ''
  try:
    start = row["start"]["value"]
  except KeyError:
    continue
    birth = ''
  try:
    end = row["end"]["value"]
  except KeyError:
    continue
    birth = ''
  try:
    death = row["death"]["value"]
  except KeyError:
    continue
    birth = ''
  try:
    nationality = row["nationalityLabel"]["value"]
  except KeyError:
    nationality = ''
  out.writerow([qid, person, position, nationality, birth, start, end, death])
