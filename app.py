from flask.helpers import url_for
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, make_response

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Key'

def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={ city }&units=metric&appid=dba04c7d88da94c4134ea7e42a481a24'
    r =  requests.get(url).json()
    return r

@app.route('/', methods = ['GET'])
def index_get():

    if (not request.cookies.get('accept')):
            flash("Aceitando cookies", 'cookie_active')

    req = request.cookies.get('cidades')

    if not req:
        cities = ['']
    else:
        cities = req.split(", ")

    weather_data = []

    if cities != ['']:

        for city in cities:

            r = get_weather_data(city)

            weather = {
                'city' : city,
                'temperature' : r['main']['temp'],
                'description' : r['weather'][0]['description'],
                'icon' : r['weather'][0]['icon']
            }

            weather_data.append(weather)
        
    return render_template('weather.html', weather_data = weather_data)

@app.route('/', methods = ['POST'])
def index_post():

    req = request.cookies.get('cidades')
    
    if not req:
        cities = []
    else:
        cities = req.split(", ")
    
    err_msg = ''
    
    new_city = request.form.get('city').capitalize()

    if new_city != '':
        if new_city:
            if new_city in cities:
                err_msg = 'Cidade já existente na base de dados!'
            else:
                new_city_data = get_weather_data(new_city)

                if new_city_data['cod'] == 200:
                    cities.append(new_city)   
                else:
                    err_msg = 'Cidade não encontrada!'
        if err_msg:
            flash(err_msg, 'error')
        else:
            flash('Cidade adicionada com sucesso!', 'succes')
    else:
        err_msg = 'Inserir o nome da cidade no campo solicitado!'
        flash(err_msg, 'error')

    res = make_response(redirect(url_for('index_get')))

    if cities != []:
        res.set_cookie('cidades', ', '.join(cities), max_age=60*60*24*365*2)

    return res

@app.route('/delete/<name>')
def delete_city(name):
    cities = request.cookies.get('cidades').split(", ")
    cities.remove(name) 

    flash(f'{ name } eliminada da base de dados!')

    res = make_response(redirect(url_for('index_get')))
    res.set_cookie('cidades', ', '.join(cities), max_age=60*60*24*365*2)

    return res

@app.route('/cookie')
def accept_cookies():

    res = make_response(redirect(url_for('index_get')))
    res.set_cookie('accept', 'true', max_age=60*60*24*365*2)

    return res
