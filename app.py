import requests
import configparser
import pymongo
from flask import Flask, render_template, request, jsonify
# template lenguaje in pycharm should be jinja2


app = Flask(__name__)


def get_db():
    """
    conexion a la DB
    :return: db con la conexion a la DB
    """
    client = pymongo.MongoClient(host='test_mongodb',
                         port=27017,
                         username='root',
                         password='pass',
                         authSource='admin')
    db = client['weather_app']
    return db


@app.route('/')
def weather_home():
    """
    Dashboard inicial
    :return:
    """
    return render_template('home.html')


@app.route('/results', methods=['POST'])
def render_results():
    """
    selección de datos importantes a mostrar.
    Se podria haber hecho una función extra para extraer esos datos.
    :return: le pasamos al template las variables seleccionadas.
    """
    zip_code = request.form['zipCode']
    data = get_weather(zip_code, get_key())
    location = data['locality']['name']
    date = data['day1']['date']
    max_tem = data['day1']['temperature_max']
    min_tem = data['day1']['temperature_min']
    weather = data['day1']['text']
    save_query(date, location, max_tem, min_tem, weather)

    return render_template('results.html', location=location, date=date, max_tem=max_tem, min_tem=min_tem,
                           weather=weather)


@app.route('/petition')
def query_db_route():
    """
    peticion a la base de datos dado un nombre de una localidad
    >>> 127.0.0.1:5000/petition?location=Baniel
    puedes usarlo con esta llamada como ejemplo ya que he introducido como mock unas ciudades.
    :return:
    """
    # He realizado este paso de argumentos asi para hacerlo de una manera distinta y no pasarlo otra vez por formulario
    location = request.args.get('ciudad', default = 'Baniel', type = str)
    db = get_db()
    _city = db.cities.find({'location': location})
    weather_list = [{'location': city['location'], 'max': city['max'], 'min': city['min'], 'weather': city['weather']} for city in _city]
    return jsonify({'city': weather_list})



def save_query(date, location, max_tem, min_tem, weather):
    """
    actualizacion de la base de datos
    :param date:
    :param location:
    :param max_tem:
    :param min_tem:
    :param weather:
    :return:
    """
    db = get_db()
    data = {
        'date': date,
        'location': location,
        'max': max_tem,
        'min': min_tem,
        'weather': weather
    }
    db.cities.insert_one(data)

def get_key():
    """
    para no tener la clave de la api en este archivo sin más
    :return:
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']


def get_weather(zip_code, key):
    """
    llamada a la api, aunque habia varias formas, elegi esta por simpleza.
    :param zip_code:
    :param key:
    :return:
    """
    url = "https://api.tutiempo.net/json/?"
    payload = {"lan": "es", "apid": key, "lid": zip_code}
    response = requests.get(url, params=payload)
    return response.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) #host='0.0.0.0', port=5000
