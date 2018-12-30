import requests
import urllib
from io import StringIO
import csv
import sys

query = """[[Category::Hackerspace]]
[[Hackerspace status::active]]
[[Website::+]]
"""
field = "Website"

#csv
url = "https://wiki.hackerspaces.org/w/index.php?title=Special%3AAsk&q=" + \
    urllib.parse.quote(query.replace("\n","")) + \
    "&po=" + \
    urllib.parse.quote(field) + \
    "&eq=yes&p%5Bformat%5D=csv&sort%5B0%5D=Modification+date&order%5B0%5D=ASC&sort_num=&order_num=ASC&p%5Blimit%5D=&p%5Boffset%5D=&p%5Blink%5D=all&p%5Bsort%5D=Modification+date&p%5Border%5D%5Basc%5D=1&p%5Bheaders%5D=show&p%5Bmainlabel%5D=&p%5Bintro%5D=&p%5Boutro%5D=&p%5Bsearchlabel%5D=...+further+results&p%5Bdefault%5D=&p%5Bsep%5D=%2C&p%5Bfilename%5D=result.csv&eq=yes"

request = requests.get(url)
stream = StringIO(request.text)
hackerspaces = csv.reader(stream, delimiter=',')
headers = next(hackerspaces, None)
print("Hackerspace,","Status,",field)
for hackerspace in hackerspaces:
    try:
        status = urllib.request.urlopen(hackerspace[1]).getcode()
    except Exception:
        status = "xxx"
    print("\"" + hackerspace[0] + "\"," + str(status) + "," + hackerspace[1])
    sys.stdout.flush()
