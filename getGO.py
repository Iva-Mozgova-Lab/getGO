#!/usr/bin/env python
import requests
import argparse
import sys
import os


parser = argparse.ArgumentParser(description='get GO-term from p.product')
parser.add_argument('-i', '--infile', help='p.product list', required =True)

args = parser.parse_args()

infile = args.infile
infile_path = args.infile

infile = os.path.splitext(infile_path)[0]
out = open(infile + '.GO', "a")


with open(infile_path) as f:
	lines = f.read().split("\n")
lines = filter(None, lines)

for line in lines:
    query = line.replace(' ', '%20')
        
    requestURL = ('https://www.ebi.ac.uk/QuickGO/services/ontology/go/search?query=' + query + '&limit=25&page=1')
    r = requests.get(requestURL, headers={ "Accept" : "application/json"})

    if not r.ok:
        r.raise_for_status()
        sys.exit()

    responseBody = [r.text]
    
    for GO in responseBody:
        Obsolete = GO.split('"isObsolete":false')[0].split('GO:')[-1].replace('",','')
        try:
            aspect = GO.split('"isObsolete":false')[1].split('"aspect":')[1].split('"')[1]
            name = GO.split('"isObsolete":false')[1].split('"name":')[1].split('"')[1]
            out.write(line + '\t' + 'GO:' + Obsolete + '\t' + name + '\t' + aspect + '\n')
        except IndexError:
            print (line)
            out.write(line + '\n') 

