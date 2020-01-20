#!/usr/bin/env python3

import urllib.request
import csv
from io import StringIO

OSIRIS_MASTER = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTmUmcYboRFnIfyHQkrmo_TRfLlLb42ve92XvPfMj05zC4FPnvcT-SW9M-3gkExn-Fe65tAXtW0rbpv/pub?output=csv&gid=0"
OSIRIS_NEWDATA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQUx7ukBGrGe6NDJJW5BTZoKKcCCKhnpgJp3tQjOxVIkcrS-riJnXKlg2F-jrc3o9sE5Rs-bJtMy47z/pub?output=csv&gid=1134814326"

dataset = {}
lookup = {}

def load_master():
    global dataset
    global lookup
    # Cols: -- Center Openings Link1 Link2 Link3 Link4 Link5 Link6 Comments ?? isDup Checksum2
    urlstream = urllib.request.urlopen(OSIRIS_MASTER)
    csvf = csv.reader(StringIO(urlstream.read().decode('utf-8')), delimiter=',')
    iter(csvf)  # Toss out headers
    for row in csvf:
        url = row[0]
        center = row[1]
        openings = row[2]
        link1 = row[3]
        link2 = row[4]
        link3 = row[5]
        link4 = row[6]
        link5 = row[7]
        link6 = row[8]
        checksum = row[12]

        node = {
            "url": row[0],
            "center": row[1],
            "openings": row[2],
            "link1": row[3],
            "link2": row[4],
            "link3": row[5],
            "link4": row[6],
            "link5": row[7],
            "link6": row[8],

        }
        dataset[checksum] = node
        lookup[link1 + link2] = checksum

def load_newdata():
    global dataset
    global lookup
    # Cols: -- Center Openings Link1 Link2 Link3 Link4 Link5 Link6 Comments isDup ??
    urlstream = urllib.request.urlopen(OSIRIS_NEWDATA)
    csvf = csv.reader(StringIO(urlstream.read().decode('utf-8')), delimiter=',')
    for row in csvf:
        url = row[0]
        center = row[1]
        openings = row[2]
        link1 = row[3]
        link2 = row[4]
        link3 = row[5]
        link4 = row[6]
        link5 = row[7]
        link6 = row[8]
        checksum = link1 + link2 + link3 + link4 + link5 + link6

        node = {
            "url": row[0],
            "center": row[1],
            "openings": row[2],
            "link1": row[3],
            "link2": row[4],
            "link3": row[5],
            "link4": row[6],
            "link5": row[7],
            "link6": row[8],

        }
        dataset[checksum] = node
        lookup[link1 + link2] = checksum

if __name__ == "__main__":
    load_master()
    load_newdata()
    print("---- Destiny 2 Corridors dupe checker 19/01/20 ----")
    print("\tType 'exit' to quit")
    print("\tType 'reload' to refresh data from spreadsheets")
    print("Enter first 2 links (i.e. PSCDTPHTBHCSBH) or a full checksum (i.e. PSCDTPHTBHCSBHDTDTTSCHCHSTDHBPSSHBCTSCHHST)")
    while True:
        check_in = input("> ")
        if (check_in == 'exit'):
            exit(0)
        if (check_in == 'reload'):
            load_master()
            load_newdata()
            print("Data reloaded")
            continue

        check_in = "".join(check_in.split())
        
        # If 2 links found in lookup, set check_in to the full checksum
        if check_in in lookup:
            check_in = lookup[check_in]
        if check_in in dataset:
            dupe = dataset[check_in]
            print("Checksum found - You have a dupe")
            print("{}\n{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(dupe['url'], dupe['center'], dupe['openings'], dupe['link1'], dupe['link2'], dupe['link3'], dupe['link4'], dupe['link5'], dupe['link6']))
        else:
            print("Not found - Unique")