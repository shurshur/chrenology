#!/usr/bin/env python
import sys
import os
import csv

out = csv.writer(open("output.csv","w"), delimiter=",")

# Параметры для поиска параллелей по продолжительности жизни
#min_series_size = 5
#min_size = 5
#max_size = 10
#max_diff = 2
#year_index1 = 4
#year_index2 = 7

# Параметры для поиска параллелей по длительности правления
min_series_size = 7
min_size = 7
max_size = 15
max_diff = 5
year_index1 = 5
year_index2 = 6

print ("Load data...")

f = open("data.csv","r")
inf = csv.reader(f, delimiter=",", quotechar='"')

data = {}
gdata = {}
series = {}

duplicate_count = 0
nonationality_count = 0
total_count = 0
valid_count = 0

first = True
for r in inf:
  if first:
    first = False
    continue
  qid, person, position, nationality, birth, start, end, death = r
  total_count += 1
  if qid in data:
    #print (f"WARNING skip duplicate {r}")
    duplicate_count += 1
    continue
  data[qid] = r
  if nationality == '':
    #print (f"WARNING skip nonationality {r}")
    nonationality_count += 1
    continue
  valid_count += 1
  if nationality not in gdata: gdata[nationality] = []
  gdata[nationality].append(qid)

  for nationality,s in gdata.items():
    if len(s) < min_series_size: continue
    series[nationality] = sorted(s, key=lambda qid:(data[qid][year_index1],data[qid][year_index2]))

selected_count = 0
for nationality, s in series.items():
  selected_count += len(s)
  print (f" Series {len(s):3d} {nationality}")

print (f"Stat: total_count={total_count} valid_count={valid_count} duplicate_count={duplicate_count} nonationality_count={nonationality_count} selected_count={selected_count} gdata={len(gdata)} series={len(series)}")

for size in range(min_size, max_size+1):
  size_found_count = 0
  print (f"Analyze size={size}")
  for n1, s1 in series.items():
    for ss1 in range(0,len(s1)-size+1):
      #ss = s1[ss1:ss1+size]
      ls1 = [int(data[qid][year_index2])-int(data[qid][year_index1]) for qid in s1[ss1:ss1+size]]
      for n2, s2 in series.items():
        if n2 <= n1: continue
        for ss2 in range(0,len(s2)-size+1):
          ls2 = [int(data[qid][year_index2])-int(data[qid][year_index1]) for qid in s2[ss2:ss2+size]]
          good = True
          metric = 0
          for i,v in enumerate(ls1):
            metric += abs(ls2[i]-v)
            if abs(ls2[i]-v) > max_diff:
              good = False
              break
          if good:
            metric = metric*1./size
            print (f"Found match size={size} metric={metric} ls1={ls1} ls2={ls2}")
            out.writerow([f"size={size} metric={metric} ls1={ls1} ls2={ls2}"])
            out.writerow([f"Серия 1"])
            for qid in s1[ss1:ss1+size]:
              print (f" S1 {qid} {data[qid]}")
              out.writerow(data[qid])
            out.writerow([f"Серия 2"])
            for qid in s2[ss2:ss2+size]:
              print (f" S2 {qid} {data[qid]}")
              out.writerow(data[qid])
            out.writerow([""])
            size_found_count += 1
  if not size_found_count:
    print (f"Nothing found with size={size}, stop searching")
    break
