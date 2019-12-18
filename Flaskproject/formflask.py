import urllib, requests, socket, urllib3, re, lxml, io, bs4, scrapy, sqlite3, pandas, os
import urllib.request
from bs4 import BeautifulSoup
import sqlite3

from flask import Flask, request, render_template,jsonify
app = Flask(__name__, template_folder='templates')


def cur_execute1(data, *args):
    con = sqlite3.connect('weather.db')
    with con:
        cur = con.cursor()
        cur.execute(data, args)
        con.commit()

cur_execute1('DROP TABLE IF EXISTS data')
cur_execute1("CREATE TABLE data(Date TEXT, CityANDTemp TEXT)")


def cur_execute2(data, *args):
    con = sqlite3.connect('capitals.db')
    with con:
        cur = con.cursor()
        cur.execute(data, args)
        con.commit()

cur_execute2('DROP TABLE IF EXISTS data')
cur_execute2("CREATE TABLE data(City TEXT, period TEXT, Days TEXT)")

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
            cur_execute1("INSERT INTO data VALUES(?, ?)", selected_date[0], elem)
            return combine
    else:
        combine = 'data was not found'
        return combine


def capitals(city, limit):
    if os.path.isfile('capitals.txt'):
        os.remove('capitals.txt')

    MOSCOW = 'https://www.worldweatheronline.com/moscow-weather/moscow-city/ru.aspx'
    OTTAWA = 'https://www.worldweatheronline.com/ottawa-weather/ontario/ca.aspx'
    WASHIGNTON = 'https://www.worldweatheronline.com/washington-weather/district-of-columbia/us.aspx'
    LONDON = 'https://www.worldweatheronline.com/london-weather/city-of-london-greater-london/gb.aspx'
    KIEV = 'https://www.worldweatheronline.com/kiev-weather/kyyivska-oblast/ua.aspx'
    ABUDHABI = 'https://www.worldweatheronline.com/abu-dhabi-weather/abu-dhabi/ae.aspx'
    CAIRO = 'https://www.worldweatheronline.com/cairo-weather/al-qahirah/eg.aspx'
    DAMASCUS = 'https://www.worldweatheronline.com/damascus-weather/dimashq/sy.aspx'
    BERLIN = 'https://www.worldweatheronline.com/berlin-weather/berlin/de.aspx'
    ROME = 'https://www.worldweatheronline.com/rome-weather/lazio/it.aspx'
    BUDAPEST = 'https://www.worldweatheronline.com/budapest-weather/budapest/hu.aspx'
    BAKU = 'https://www.worldweatheronline.com/baku-weather/baki/az.aspx'
    YEREVAN = 'https://www.worldweatheronline.com/yerevan-weather/yerevan/am.aspx'
    VIENNA = 'https://www.worldweatheronline.com/vienna-weather/wien/at.aspx'
    BUENOSAIRES = 'https://www.worldweatheronline.com/buenos-aires-weather/distrito-federal/ar.aspx'
    BRUSSELS = 'https://www.worldweatheronline.com/brussels-weather/be.aspx'
    BEIJING = 'https://www.worldweatheronline.com/beijing-weather/beijing/cn.aspx'
    LISBON = 'https://www.worldweatheronline.com/lisbon-weather/lisboa/pt.aspx'
    SYDNEY = 'https://www.worldweatheronline.com/sydney-weather/new-south-wales/au.aspx'
    RIYADH = 'https://www.worldweatheronline.com/riyadh-weather/ar-riyad/sa.aspx'
    ANKARA = 'https://www.worldweatheronline.com/ankara-weather/ankara/tr.aspx'
    TIRANE = 'https://www.worldweatheronline.com/tirana-weather/tirane/al.aspx'
    MINSK = 'https://www.worldweatheronline.com/minsk-weather/minsk/by.aspx'
    HELSINKI = 'https://www.worldweatheronline.com/helsinki-weather/southern-finland/fi.aspx'
    ATHENS = 'https://www.worldweatheronline.com/athens-weather/attica/gr.aspx'
    DUBLIN = 'https://www.worldweatheronline.com/coultry-weather/dublin/ie.aspx'
    BEIRUT = 'https://www.worldweatheronline.com/beirut-weather/beyrouth/lb.aspx'
    MONACO = 'https://www.worldweatheronline.com/monaco-ville-weather/mc.aspx'
    ISLAMABAD = 'https://www.worldweatheronline.com/islamabad-weather/islamabad/pk.aspx'
    SEOUL = 'https://www.worldweatheronline.com/seoul-weather/kr.aspx'

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

    selected_city = urllib.request.urlopen(the_city[city])
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


    days = {i: DATA[i - 1][:9] + ",&nbsp;""&nbsp;High/Low:" + DATA[i - 1][10:] + ",&nbsp;&nbsp;" + STATUS[i - 1] + "&nbsp;&nbsp;" + "<br/><br/>" for i in range(1, 15)}

    Days = {i: DATA[i - 1][:9] + ", " + DATA[i - 1][10:] + ", " + STATUS[i - 1] + "|" for i in range(1, 15)}

    periods = {i: DATA[0][:9] + "-" + DATA[i - 1][:9] for i in range(3, 15)}

    Total4 = days[1] + days[2] + days[3] + days[4]
    Total7 = days[1] + days[2] + days[3] + days[4] + days[5] + days[6] + days[7]
    Total10 = days[1] + days[2] + days[3] + days[4] + days[5] + days[6] + days[7] + days[8] + days[9] + days[10]
    Total14 = days[1] + days[2] + days[3] + days[4] + days[5] + days[6] + days[7] + days[8] + days[9] + days[10] + days[11] + days[12] + days[13] + days[14]

    total4 = Days[1] + Days[2] + Days[3] + Days[4]
    total7 = Days[1] + Days[2] + Days[3] + Days[4] + Days[5] + Days[6] + Days[7]
    total10 = Days[1] + Days[2] + Days[3] + Days[4] + Days[5] + Days[6] + Days[7] + Days[8] + Days[9] + Days[10]
    total14 =  Days[1] + Days[2] + Days[3] + Days[4] + Days[5] + Days[6] + Days[7] + Days[8] + Days[9] + Days[10] + Days[11] + Days[12] + Days[13] + Days[14]

    con = sqlite3.connect("capitals.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    the_option = {
        '4 days': (periods[4], Total4, total4),
        'a week': (periods[7], Total7, total7),
        '10 days': (periods[10], Total10, total10),
        '2 weeks': (periods[14], Total14, total14)}

    period, Total1, Total2 = the_option[limit]

    cur.execute('''SELECT City, period FROM data WHERE City=? AND period=? ''', (PLACE[0], period))
    exists = cur.fetchall()
    if not exists:
        output = PLACE[0] + "&nbsp;&nbsp;" + period + "<br/><br/>" + Total1
        cur_execute2("INSERT INTO data VALUES(?, ?, ?)", PLACE[0], period, Total2)
        print("not exists")
        return output
    else:

        cur.execute('''SELECT City, period, Days FROM data WHERE City=? AND period=? AND Days=?''', (PLACE[0], period, Total2))
        exists1 = cur.fetchall()
        for row in exists1:
            # return tuple(row)
            PLACE[0], period, Total2 = row
            return "From your History..." + "<br/><br/>" +PLACE[0], period + "<br/><br/>" + Total2


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


@app.route('/database2')
def database2():
    con = sqlite3.connect("capitals.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT data.City, data.period, data.Days FROM data")

    rows = cur.fetchall();
    return render_template("database2.html", rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
