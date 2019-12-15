import urllib, requests, socket, urllib3, re, lxml, io, bs4, scrapy, sqlite3, pandas, os
import urllib.request
from bs4 import BeautifulSoup
import sqlite3

from flask import Flask, request, render_template,jsonify
app = Flask(__name__, template_folder='templates')


def cur_execute(data, *args):
    con = sqlite3.connect('weather.db')
    with con:
        cur = con.cursor()
        cur.execute(data, args)
        con.commit()


cur_execute('DROP TABLE IF EXISTS data')
cur_execute("CREATE TABLE data(Date TEXT, CityANDTemp TEXT)")
def do_something(day, city):
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

    todayTemp = []  # parsing today's forecast
    tomorrowTemp = []  # parsing tomorrow's forecast
    aftertomorrowTemp = []  # parsing aftertomorrow's forecast
    for row in soup.select('tbody > tr'):
        temp = row.select('td')
        city2 = row.select('th')
        todayTemp.append(
            city2[0].text + ": Max " + temp[1].text + " °C, " + "Min " + temp[2].text + " °C"
        )

        tomorrowTemp.append(
            city2[0].text + ": Max " + temp[4].text + " °C, " + "Min " + temp[5].text + " °C"
        )

        aftertomorrowTemp.append(
            city2[0].text + ": Max " + temp[7].text + " °C, " + "Min " + temp[8].text + " °C"
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

    dateOFtoday = []  # parsing today's date
    dateOFtomorrow = []  # parsing tomorrow's date
    dateOFaftertomorrow = []  # parsing aftertomorrow's date
    for row in soup.select('thead > tr'):
        date = row.select('th')
        dateOFtoday.append(
            date[1].text
        )

        dateOFtomorrow.append(
            date[2].text
        )

        dateOFaftertomorrow.append(
            date[3].text
        )


    if day != 'Today' and day != 'Tomorrow' and day != 'Aftertomorrow':
        combine = 'OoOps!, wrong input'
        return combine


    the_day = {
        'Today': (todayTemp, dateOFtoday),
        'Tomorrow': (tomorrowTemp, dateOFtomorrow),
        'Aftertomorrow': (aftertomorrowTemp, dateOFaftertomorrow)}

    selected_temp, selected_date = the_day[day]
    for elem in selected_temp:
        if city.lower() in elem or city.upper() in elem:
            combine = selected_date[0] + ",  " + elem
            cur_execute("INSERT INTO data VALUES(?, ?)", selected_date[0], elem)
            return combine
    else:
        combine = 'data was not found'
        return combine


def capitals(city, limit):
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

    if city not in the_city.keys():
        output = "no information available for this city!"
        return output

    if limit != '4 days' and limit != 'a week' and limit != '10 days' and limit != "2 weeks":
        output ='OoOps!, wrong input'
        return output

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
    # IMAGES = []
    STATUS = []
    cities = soup.find_all("div", class_="city_name2")
    data = soup.find_all("div", class_="carousel-cell well text-center")
    # images = soup.findAll("div", class_="carousel-cell well text-center")
    status = soup.findAll("div", class_="carousel-cell well text-center")

    for div in cities:
        PLACE.append(div.text)

    for div in data:
        DATA.append(div.text)

    # for div in images:
    #     IMAGES.append(div.img.get('data-src'))


    for div in status:
        STATUS.append(div.img.get('title'))

    day1 = DATA[0][:9] + ",&nbsp;""&nbsp;High/Low:" + DATA[0][10:] + ",&nbsp;&nbsp;" + STATUS[0] + "&nbsp;&nbsp;" + "<br/><br/>"
    day2 = DATA[1][:9] + ",&nbsp;""&nbsp;High/Low:" + DATA[1][10:] + ",&nbsp;&nbsp;" + STATUS[1] + "&nbsp;&nbsp;" + "<br/><br/>"
    day3 = DATA[2][:9] + ",&nbsp;""&nbsp;High/Low:" + DATA[2][10:] + ",&nbsp;&nbsp;" + STATUS[2] + "&nbsp;&nbsp;" + "<br/><br/>"
    day4 = DATA[3][:9] + ",&nbsp;""&nbsp;High/Low:" + DATA[3][10:] + ",&nbsp;&nbsp;" + STATUS[3] + "&nbsp;&nbsp;" + "<br/><br/>"
    day5 = DATA[4][:9] + ",&nbsp;""&nbsp;High/Low:" + DATA[4][10:] + ",&nbsp;&nbsp;" + STATUS[4] + "&nbsp;&nbsp;" + "<br/><br/>"
    day6 = DATA[5][:9] + ",&nbsp;""&nbsp;High/Low:" + DATA[5][10:] + ",&nbsp;&nbsp;" + STATUS[5] + "&nbsp;&nbsp;" + "<br/><br/>"
    day7 = DATA[6][:9] + ",&nbsp;""&nbsp;High/Low:" + DATA[6][10:] + ",&nbsp;&nbsp;" + STATUS[6] + "&nbsp;&nbsp;" + "<br/><br/>"
    day8 = DATA[7][:9] + ",&nbsp;""&nbsp;High/Low:" + DATA[7][10:] + ",&nbsp;&nbsp;" + STATUS[7] + "&nbsp;&nbsp;" + "<br/><br/>"
    day9 = DATA[8][:9] + ",&nbsp;""&nbsp;High/Low:" + DATA[8][10:] + ",&nbsp;&nbsp;" + STATUS[8] + "&nbsp;&nbsp;" + "<br/><br/>"
    day10 = DATA[9][:9] + ",&nbsp;""&nbsp;High/Low:" + DATA[9][10:] + ",&nbsp;&nbsp;" + STATUS[9] + "&nbsp;&nbsp;" + "<br/><br/>"
    day11 = DATA[10][:9] + ",&nbsp;""&nbsp;High/Low:" + DATA[10][10:] + ",&nbsp;&nbsp;" + STATUS[10] + "&nbsp;&nbsp;" + "<br/><br/>"
    day12 = DATA[11][:9] + ",&nbsp;""&nbsp;High/Low:" + DATA[11][10:] + ",&nbsp;&nbsp;" + STATUS[11] + "&nbsp;&nbsp;" + "<br/><br/>"
    day13 = DATA[12][:9] + ",&nbsp;""&nbsp;High/Low:" + DATA[12][10:] + ",&nbsp;&nbsp;" + STATUS[12] + "&nbsp;&nbsp;" + "<br/><br/>"
    day14 = DATA[13][:9] + ",&nbsp;""&nbsp;High/Low:" + DATA[13][10:] + ",&nbsp;&nbsp;" + STATUS[13] + "&nbsp;&nbsp;" + "<br/><br/>"

    if limit == "4 days":
        output =  PLACE[0] + "<br/><br/>" + day1 + day2 + day3 + day4
        return output
    if limit == "a week":
        output = PLACE[0] + "<br/><br/>" + day1 + day2 + day3 + day4 + day5 + day6 + day7
        return output
    if limit == "10 days":
        output = PLACE[0] + "<br/><br/>" + day1 + day2 + day3 + day4 + day5 + day6 + day7 + day8 + day9 + day10
        return output
    if limit == "2 weeks":
        output = PLACE[0] + "<br/><br/>" + day1 + day2 + day3 + day4 + day5 + day6 + day7 + day8 + day9 + day10 + day11 + day12 + day13 + day14
        return output

@app.route('/')
def home():
    return render_template('flaskApp.html')

@app.route('/joinFUNC', methods=['GET', 'POST'])
def my_form_post():
    day = request.form['day']
    city = request.form['city']
    combine = do_something(day, city)
    result = {
        "output": combine
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)

@app.route('/capitals')
def second_page():
    return render_template('capitals.html')

@app.route('/joinFUNC2', methods=['GET', 'POST'])
def my_capitals():
    city = request.form['city']
    limit = request.form['limit']
    output = capitals(city, limit)
    result = {
        "output": output
    }
    output = {str(key): value for key, value in result.items()}
    return jsonify(result=output)



@app.route('/database')
def database():
    con = sqlite3.connect("weather.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT data.Date, data.CityANDTemp FROM data")

    rows = cur.fetchall();
    return render_template("database.html", rows=rows)
#
if __name__ == '__main__':
    app.run(debug=True)
