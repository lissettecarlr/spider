from gettext import find
from bs4 import BeautifulSoup
import requests
import time
import vx
import re

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
url = "https://www.dd373.com/s-eja7u2-3fk9tg-swu6xh-c0qukc-0-0-jk5sj0-0-0-0-0-0-1-0-5-0.html"

result = requests.get(url, headers=headers)
rText = result.text
soup = BeautifulSoup(rText, 'html.parser')
# print(soup.prettify())
res = soup.find_all(class_='font12 color666 m-t5')
tempGold =[i.text for i in res if i.text.find("=") == -1]
trueGold = [i.text for i in res if i.text.find("=") != -1]
# print(tempGold)
# print(trueGold)
tempGold = list(set(tempGold))
print(tempGold)
trueGold = list(set(trueGold))
print(trueGold)

tempGoldList = []
for temp in tempGold:
    num = float(re.findall(r"\d+\.?\d*",temp)[0])
    tempGoldList.append(num)
tempGoldList.sort()
print(tempGoldList)

trueGoldList = []
for temp in trueGold:
    num = float(re.findall(r"\d+\.?\d*",temp)[1])
    trueGoldList.append(num)
trueGoldList.sort()
print(trueGoldList)

vx.post("wow", "\n官方：\n"+str(tempGoldList)+"\n 实际：\n"+str(trueGoldList))