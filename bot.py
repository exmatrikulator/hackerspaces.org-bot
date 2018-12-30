import requests
import urllib
from io import StringIO
import csv
import sys
import threading
import time

query = """[[Category::Hackerspace]]
[[Hackerspace status::active]]
[[Website::+]]
"""
field = "Website"
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
    "&po=" + \
    urllib.parse.quote(field) + \
    attributes_url

#print(url)
#exit()

class get_http_status (threading.Thread):
    def __init__(self, hackerspace):
        threading.Thread.__init__(self)
        self.hackerspace = hackerspace
    def run(self):
        try:
            status = urllib.request.urlopen(self.hackerspace[1]).getcode()
        except Exception:
            status = "xxx"
        print("\"" + self.hackerspace[0] + "\"," + str(status) + "," + self.hackerspace[1])
        sys.stdout.flush()


threads = []
request = requests.get(url)
stream = StringIO(request.text)
hackerspaces = csv.reader(stream, delimiter=',')
headers = next(hackerspaces, None)
print("Hackerspace,Status,"+field)
for hackerspace in hackerspaces:
    while threading.active_count() > 80:
        time.sleep(1)
    thread = get_http_status(hackerspace)
    thread.start()
    threads.append(thread)


for thread in threads:
    thread.join()
