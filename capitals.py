import urllib, requests, socket, urllib3, re, lxml, io, bs4, scrapy, sqlite3, pandas, os
import urllib.request
from bs4 import BeautifulSoup

if os.path.isfile('capitals.txt'):
    os.remove('capitals.txt')

MOSCOW = urllib.request.urlopen('https://www.worldweatheronline.com/moscow-weather/moscow-city/ru.aspx')
OTTAWA = urllib.request.urlopen('https://www.worldweatheronline.com/ottawa-weather/ontario/ca.aspx')
WASHIGNTON = urllib.request.urlopen('https://www.worldweatheronline.com/washington-weather/district-of-columbia/us.aspx')
LONDON = urllib.request.urlopen('https://www.worldweatheronline.com/london-weather/city-of-london-greater-london/gb.aspx')
KIEV = urllib.request.urlopen('https://www.worldweatheronline.com/kiev-weather/kyyivska-oblast/ua.aspx')
ABUDHABI = urllib.request.urlopen('https://www.worldweatheronline.com/abu-dhabi-weather/abu-dhabi/ae.aspx')
CAIRO = urllib.request.urlopen('https://www.worldweatheronline.com/cairo-weather/al-qahirah/eg.aspx')
DAMASCUS = urllib.request.urlopen('https://www.worldweatheronline.com/damascus-weather/dimashq/sy.aspx')
BERLIN = urllib.request.urlopen('https://www.worldweatheronline.com/berlin-weather/berlin/de.aspx')
ROME = urllib.request.urlopen('https://www.worldweatheronline.com/rome-weather/lazio/it.aspx')
BUDAPEST = urllib.request.urlopen('https://www.worldweatheronline.com/budapest-weather/budapest/hu.aspx')
BAKU = urllib.request.urlopen('https://www.worldweatheronline.com/baku-weather/baki/az.aspx')
YEREVAN = urllib.request.urlopen('https://www.worldweatheronline.com/yerevan-weather/yerevan/am.aspx')
VIENNA = urllib.request.urlopen('https://www.worldweatheronline.com/vienna-weather/wien/at.aspx')
BUENOSAIRES = urllib.request.urlopen('https://www.worldweatheronline.com/buenos-aires-weather/distrito-federal/ar.aspx')
BRUSSELS = urllib.request.urlopen('https://www.worldweatheronline.com/brussels-weather/be.aspx')
BEIJING = urllib.request.urlopen('https://www.worldweatheronline.com/beijing-weather/beijing/cn.aspx')
LISBON = urllib.request.urlopen('https://www.worldweatheronline.com/lisbon-weather/lisboa/pt.aspx')
SYDNEY = urllib.request.urlopen('https://www.worldweatheronline.com/sydney-weather/new-south-wales/au.aspx')
RIYADH = urllib.request.urlopen('https://www.worldweatheronline.com/riyadh-weather/ar-riyad/sa.aspx')
ANKARA = urllib.request.urlopen('https://www.worldweatheronline.com/ankara-weather/ankara/tr.aspx')
TIRANE = urllib.request.urlopen('https://www.worldweatheronline.com/tirana-weather/tirane/al.aspx')
MINSK = urllib.request.urlopen('https://www.worldweatheronline.com/minsk-weather/minsk/by.aspx')
HELSINKI = urllib.request.urlopen('https://www.worldweatheronline.com/helsinki-weather/southern-finland/fi.aspx')
ATHENS = urllib.request.urlopen('https://www.worldweatheronline.com/athens-weather/attica/gr.aspx')
DUBLIN = urllib.request.urlopen('https://www.worldweatheronline.com/coultry-weather/dublin/ie.aspx')
BEIRUT = urllib.request.urlopen('https://www.worldweatheronline.com/beirut-weather/beyrouth/lb.aspx')
MONACO = urllib.request.urlopen('https://www.worldweatheronline.com/monaco-ville-weather/mc.aspx')
ISLAMABAD = urllib.request.urlopen('https://www.worldweatheronline.com/islamabad-weather/islamabad/pk.aspx')
SEOUL = urllib.request.urlopen('https://www.worldweatheronline.com/seoul-weather/kr.aspx')


the_city = {
    'Moscow': (MOSCOW),
    'Ottawa': (OTTAWA),
    'Washington': (WASHIGNTON),
    'London': (LONDON),
    'Kiev': (KIEV),
    'Abu dhabi': (ABUDHABI),
    'Cairo': (CAIRO),
    'Damascus': (DAMASCUS),
    'Berlin': (BERLIN),
    'Rome': (ROME),
    'Budapest': (BUDAPEST),
    'Baku': (BAKU),
    'Yerevan': (YEREVAN),
    'Vienna': (VIENNA),
    'Buenos Aires': (BUENOSAIRES),
    'Brussels': (BRUSSELS),
    'Beijing': (BEIJING),
    'Lisbon': (LISBON),
    'Sydney': (SYDNEY),
    'Riyadh': (RIYADH),
    'Ankara': (ANKARA),
    'Tirane': (TIRANE),
    'Minsk': (MINSK),
    'Helsinki': (HELSINKI),
    'Athens': (ATHENS),
    'Dublin': (DUBLIN),
    'Beirut': (BEIRUT),
    'Monaco': (MONACO),
    'Islamabad': (ISLAMABAD),
    'Seoul': (SEOUL)
}
print("Type the name of city that you wish to get information about")
city = str(input())

print("for how many days you want to check the forecast? press 4, 7, 10 or 14 ")
limit = str(input())

if city not in the_city.keys():
    print("no information available for this city!")
    exit()

if limit != '4' and limit != '7' and limit != '10' and limit != "14":
    print('OoOps!, wrong input')
    exit()

selected_city = the_city[city]
html = selected_city.read()
html = html.decode('utf-8')

with open('capitals.txt', 'w', encoding='utf-8') as f:
    f.write(html)

with open('capitals.txt', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'lxml')

PLACE = []
DATA = []
IMAGES = []
STATUS = []
cities = soup.find_all("div", class_="city_name2")
data = soup.find_all("div", class_="carousel-cell well text-center")
images = soup.findAll("div", class_="carousel-cell well text-center")
status = soup.findAll("div", class_="carousel-cell well text-center")

for div in cities:
    PLACE.append(div.text)
print(PLACE[0])

for div in data:
    DATA.append(div.text)

for div in images:
    IMAGES.append(div.img.get('data-src'))

for div in status:
    STATUS.append(div.img.get('title'))


if limit == "4":
    print(DATA[0][:9], DATA[0][10:], STATUS[0], IMAGES[0], sep=', ')
    print(DATA[1][:9], DATA[1][10:], STATUS[1], IMAGES[1], sep=', ')
    print(DATA[2][:9], DATA[2][10:], STATUS[2], IMAGES[2], sep=', ')
    print(DATA[3][:9], DATA[3][10:], STATUS[3], IMAGES[3], sep=', ')
if limit == "7":
    print(DATA[0][:9], DATA[0][10:], STATUS[0], IMAGES[0], sep=', ')
    print(DATA[1][:9], DATA[1][10:], STATUS[1], IMAGES[1], sep=', ')
    print(DATA[2][:9], DATA[2][10:], STATUS[2], IMAGES[2], sep=', ')
    print(DATA[3][:9], DATA[3][10:], STATUS[3], IMAGES[3], sep=', ')
    print(DATA[4][:9], DATA[4][10:], STATUS[4], IMAGES[4], sep=', ')
    print(DATA[5][:9], DATA[5][10:], STATUS[5], IMAGES[5], sep=', ')
    print(DATA[6][:9], DATA[6][10:], STATUS[6], IMAGES[6], sep=', ')
if limit == "10":
    print(DATA[0][:9], DATA[0][10:], STATUS[0], IMAGES[0], sep=', ')
    print(DATA[1][:9], DATA[1][10:], STATUS[1], IMAGES[1], sep=', ')
    print(DATA[2][:9], DATA[2][10:], STATUS[2], IMAGES[2], sep=', ')
    print(DATA[3][:9], DATA[3][10:], STATUS[3], IMAGES[3], sep=', ')
    print(DATA[4][:9], DATA[4][10:], STATUS[4], IMAGES[4], sep=', ')
    print(DATA[5][:9], DATA[5][10:], STATUS[5], IMAGES[5], sep=', ')
    print(DATA[6][:9], DATA[6][10:], STATUS[6], IMAGES[6], sep=', ')
    print(DATA[7][:9], DATA[7][10:], STATUS[7], IMAGES[7], sep=', ')
    print(DATA[8][:9], DATA[8][10:], STATUS[8], IMAGES[8], sep=', ')
    print(DATA[9][:9], DATA[9][10:], STATUS[9], IMAGES[9], sep=', ')
if limit == "14":
    print(DATA[0][:9], DATA[0][10:], STATUS[0], IMAGES[0], sep=', ')
    print(DATA[1][:9], DATA[1][10:], STATUS[1], IMAGES[1], sep=', ')
    print(DATA[2][:9], DATA[2][10:], STATUS[2], IMAGES[2], sep=', ')
    print(DATA[3][:9], DATA[3][10:], STATUS[3], IMAGES[3], sep=', ')
    print(DATA[4][:9], DATA[4][10:], STATUS[4], IMAGES[4], sep=', ')
    print(DATA[5][:9], DATA[5][10:], STATUS[5], IMAGES[5], sep=', ')
    print(DATA[6][:9], DATA[6][10:], STATUS[6], IMAGES[6], sep=', ')
    print(DATA[7][:9], DATA[7][10:], STATUS[7], IMAGES[7], sep=', ')
    print(DATA[8][:9], DATA[8][10:], STATUS[8], IMAGES[8], sep=', ')
    print(DATA[9][:9], DATA[9][10:], STATUS[9], IMAGES[9], sep=', ')
    print(DATA[10][:9], DATA[10][10:], STATUS[10], IMAGES[10], sep=', ')
    print(DATA[11][:9], DATA[11][10:], STATUS[11], IMAGES[11], sep=', ')
    print(DATA[12][:9], DATA[12][10:], STATUS[12], IMAGES[12], sep=', ')
    print(DATA[13][:9], DATA[13][10:], STATUS[13], IMAGES[13], sep=', ')
