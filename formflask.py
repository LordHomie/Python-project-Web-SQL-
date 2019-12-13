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



@app.route('/')
def home():
    return render_template('flaskApp.html')


@app.route('/join', methods=['GET', 'POST'])
def my_form_post():
    # if request.method == "POST":
        day = request.form['day']
        city = request.form['city']
        combine = do_something(day, city)
        result = {
            "output": combine
        }
        result = {str(key): value for key, value in result.items()}
        return jsonify(result=result)

@app.route('/database')
def database():
    con = sqlite3.connect("weather.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT data.Date, data.CityANDTemp FROM data")

    rows = cur.fetchall();
    return render_template("database.html", rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
