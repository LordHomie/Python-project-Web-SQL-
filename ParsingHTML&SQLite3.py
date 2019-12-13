import urllib, requests, socket, urllib3, re, lxml, io, bs4, scrapy, sqlite3, pandas, os
import urllib.request
from bs4 import BeautifulSoup
import sqlite3

if os.path.isfile('weather.txt'):
    os.remove('weather.txt')

response = urllib.request.urlopen('https://mgm.gov.tr/eng/forecast-some-world-cities.aspx')
html = response.read()
html = html.decode('utf-8')

with open('weather.txt', 'w', encoding='utf-8') as f:
    f.write(html)

with open('weather.txt', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'lxml')

today = [] # parsing today's forecast
tomorrow = [] # parsing tomorrow's forecast
aftertomorrow = [] # parsing aftertomorrow's forecast
for row in soup.select('tbody > tr'):
    temp = row.select('td')
    city = row.select('th')
    today.append(
        city[0].text + ": Max " + temp[1].text + " °C, " + "Min " + temp[2].text + " °C"
    )

    tomorrow.append(
        city[0].text + ": Max " + temp[4].text + " °C, " + "Min " + temp[5].text + " °C"
    )

    aftertomorrow.append(
        city[0].text + ": Max " + temp[7].text + " °C, " + "Min " + temp[8].text + " °C"
    )

# for elem in today:
#     print(elem)
# print(today[0])

# for elem in tomorrow:
#     print(elem)
# print(tomorrow[0])

# for elem in aftertomorrow:
#     print(elem)
# print(aftertomorrow[0])

today1 = []  # parsing today's date
tomorrow1 = []  # parsing tomorrow's date
aftertomorrow1 = []  # parsing aftertomorrow's date
for row in soup.select('thead > tr'):
    date = row.select('th')
    today1.append(
        date[1].text
    )

    tomorrow1.append(
        date[2].text
    )

    aftertomorrow1.append(
        date[3].text
    )

# print(today1[0])
# print(tomorrow1[0])
# print(aftertomorrow1[0])

def cur_execute(data, *args):
    con = sqlite3.connect('weather.db')
    with con:
        cur = con.cursor()
        cur.execute(data, args)
        con.commit()
cur_execute('DROP TABLE IF EXISTS data')
cur_execute("CREATE TABLE data(Date TEXT, CityANDTemp TEXT)")

print("Welcome to the Express Forecast Agency")
while True:
    print("press '1' to get today's forecast OR '2' for tomorrow's forecast OR '3' for aftertomorrow's forecast")
    day = str(input())

    if day != '1' and day != '2' and day != '3':
        print('OoOps!, wrong input')
        exit()


    print('type the name of the city')
    city = str(input())

    the_day = {
        '1': (today, today1),
        '2': (tomorrow, tomorrow1),
        '3': (aftertomorrow, aftertomorrow1)}

    selected_day, selected_day1 = the_day[day]
    for elem in selected_day:
        if city.lower() in elem or city.upper() in elem:
            print(selected_day1[0])
            print(elem)
            cur_execute("INSERT INTO data VALUES(?, ?)", selected_day1[0], elem)
            break
    else:
        print('data was not found')

    print('to display history press "d" OR "c" to continue OR "e" to exit')
    option= str(input())
    if option =='d':
        def read_lines(conn):
            query = "SELECT data.Date, data.CityANDTemp FROM data"
            cur = conn.cursor()
            cur.execute(query)

            for row in cur:
                Date, CityANDTemp = row
                print(Date, end=', ')
                print(CityANDTemp)


        with sqlite3.connect('weather.db') as conn:
            read_lines(conn)
            exit()
    if option == 'c':
        pass
    if option == 'e':
        exit()
