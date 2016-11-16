import numpy as np
import os, sys
import json

#here we read the files line by line and do a lot of trimming
paths = ['Oma_alue_2015.csv', 'Oma_alue_2012.csv', 'ASUINALUE_2009.csv', 'ASUINALUE_2006.csv']
for path in paths:
    f = open('data/' + path)
    lines = f.readlines()[9:]
    f.close()

    data = {}
    curr_area = None
    for line in lines:
        splitline = line.strip().split(";")
        kpi = splitline[1] #Frequency, Percent, or Row Pct
        vals = splitline[2:] # ";;" at the end of each line??

        vals_ob = {i:0.0 if not val else float(val.replace(",",".")) for (i,val) in enumerate(vals)}
        vals = vals_ob

        if not splitline[0]:
            data[curr_area][kpi] = vals
            continue
        curr_area = splitline[0]
        area_ob = {kpi: vals}
        data[curr_area] = area_ob

    # DEBUG
    # print data.keys()
    for area in data:
        for kpi in data[area]:
            # print len(data[area][kpi][-2:])
            # print data[area][kpi][-2:]
            # if (data[area][kpi][-2]) or (data[area][kpi][-1]):
            #     print len(data[area][kpi])
            # print kpi, len(data[area][kpi].keys())
            # print kpi, data[area][kpi]
            if kpi == "Row Pct":
                print kpi, data[area][kpi]
    # /DEBUG

    with open('data/' + path + '.json', 'w') as outf:
        json.dump(data, outf, indent=4)

allyears = {}

# merge resulting json files, by area
for file in [f for f in os.listdir('./data') if f.split('.')[-1] == 'json']:
    if "by_year" in file:
        continue
    year = file.split('.')[0].split('_')[-1]
    print(year)
    j = json.load(open(file))
    for area in j:
        if area not in allyears:
            allyears[area] = {}
        try:
            allyears[area][year] = j[area]['Row Pct']
        except:
            print(year, area, j[area])
with open('data/by_year.json', 'w') as out:
    json.dump(allyears, out, indent=4)

# finally form the values we want (SAFE and UNSAFE)
with open('data/by_year.json', 'r') as jsonfile:
    d = json.load(jsonfile)
    for area in d:
        for year in d[area]:
            year_ob = {}
            if year == '2006':
                safe = d[area][year]['0']
                unsafe = d[area][year]['1']
            elif year == '2009':
                safe = d[area][year]['1']
                unsafe = d[area][year]['2']
            elif year == '2012':
                safe = d[area][year]['1']
                unsafe = d[area][year]['2'] + d[area][year]['3'] + d[area][year]['4']
            elif year == '2015':
                safe = d[area][year]['1']
                unsafe = d[area][year]['2'] + d[area][year]['3']
            year_ob['safe'] = safe
            year_ob['unsafe'] = unsafe
            d[area][year] = year_ob

    with open('data/safe_by_year.json', 'w') as finalout:
        json.dump({'data':d}, finalout, ensure_ascii=False, encoding='utf-8')
