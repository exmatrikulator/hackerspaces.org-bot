#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import urllib
from io import StringIO
import csv
import sys
import threading
import time
import json

query = """[[Category::Hackerspace]]
[[Hackerspace status::active]]
"""
fields = ("Website","SpaceAPI")
attributes = {}
attributes["format"] = "csv"
attributes["limit"] = "500"
attributes["sort"] = "Modification date"
attributes["oder"] = "asc"


attributes_url = ""
for key, value in attributes.items():
    attributes_url +=  "&p%5b" + urllib.parse.quote(key) + "%5d=" + urllib.parse.quote(value)

#csv
url = "https://wiki.hackerspaces.org/w/index.php?title=Special%3AAsk&q=" + \
    urllib.parse.quote(query.replace("\n","")) + \
    "&po=%3F" + \
    "%0D%0A%3F".join(fields).replace(" ","%20") + \
    "%0D%0A" + \
    attributes_url

#print(url)
#exit()

class get_http_status (threading.Thread):
    def __init__(self, hackerspace):
        threading.Thread.__init__(self)
        self.hackerspace = hackerspace
    def run(self):
        try:
            status = str(urllib.request.urlopen(self.hackerspace[1], timeout=10).getcode())
        except Exception:
            status = "xxx"

        if status != "200":
            #print("\"" + self.hackerspace[0] + "\"," + status + "," + self.hackerspace[1])
            #sys.stdout.flush()
            website_file.write("\"" + self.hackerspace[0] + "\"," + status + "," + self.hackerspace[1] + "\n")

class check_json (threading.Thread):
    def __init__(self, hackerspace):
        threading.Thread.__init__(self)
        self.hackerspace = hackerspace
    def run(self):
        try:
            json.loads(urllib.request.urlopen(self.hackerspace[2], timeout=10).read())
            status = True
        except Exception:
            status = False

        if status != True:
            #print("\"" + self.hackerspace[0] + "\"," + self.hackerspace[2])
            #sys.stdout.flush()
            spaceapi_file.write("\"" + self.hackerspace[0] + "," + self.hackerspace[2] + "\n")


website_file = open('website.csv', 'w')
spaceapi_file = open('spaceapi.csv', 'w')

threads = []
request = requests.get(url)
stream = StringIO(request.text)
hackerspaces = csv.reader(stream, delimiter=',')
headers = next(hackerspaces, None)
check_count = 0
for hackerspace in hackerspaces:
    print("already started %s checks" % check_count,  end="\r")
    while threading.active_count() > 80:
        time.sleep(1)
    if(hackerspace[1]):
        thread = get_http_status(hackerspace)
        thread.start()
        threads.append(thread)
        check_count += 1
    if(hackerspace[2]):
        thread = check_json(hackerspace)
        thread.start()
        threads.append(thread)
        check_count += 1

while threading.active_count() > 1:
    print("started %s checks, waiting for %s checks" % (check_count, threading.active_count()),  end="\r")
    time.sleep(1)

for thread in threads:
    thread.join()

print("done")
