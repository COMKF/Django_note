import re
import requests

r = requests.get("https://www.pgexercises.com/questions/basic/selectall.html")
url = r.url

reg = re.compile(r'<h3>(.+?)</h3>')
text = reg.findall(r.text)
with open('123.txt', 'a') as f:
    f.write(text[0]+'\n')

reg = re.compile(r'<h3>Q.+?</h3>(.+?)</div')
text2 = reg.findall(r.text)
with open('123.txt', 'a') as f:
    f.write(text2[0]+'\n')

with open('123.txt', 'a') as f:
    f.write(text[2][:text[2].find('<')-1]+'\n')

reg = re.compile(r'<pre.*\n(.+?)\s+</pre>')
text3 = reg.findall(r.text)
with open('123.txt', 'a') as f:
    f.write(text3[0]+'\n')
