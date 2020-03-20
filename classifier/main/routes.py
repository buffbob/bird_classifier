from flask import render_template, Blueprint
import requests

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template('main/home.html', title="Home")


@main.route("/getting_started")
def start():
    return render_template("main/getting_started.html")

@main.route('/weather')
def weather():
    api_key = "b60a8f05df9bcdb1d7f9218c6029beaa"
    city = "Denver"
    url = "http://apiu.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}".format(city,api_key)

    r = requests.get(url).json()

    cities=[]
    data = {
        "city":r["name"],
        "temp":r['main']['temp'],
        "description":r['weather'][0]['description'],
        "icon":r['weather'][0]['icon']
    }
    cities.append(data)
    return render_template('main/weather.html', weather_data=cities)

