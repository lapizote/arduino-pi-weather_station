# app.py
from flask import Flask, render_template, request, redirect, session
from mysql.connector import Error
import mysql.connector
from datetime import datetime
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("weather_station.log"),
        logging.StreamHandler(sys.stdout)  # Sends logs to standard output (screen)
    ]
)

logger = logging.getLogger(__name__)

def getHeatIndex(T, RH, fahrenheit=False):
    index = 0
    if (fahrenheit):
        index = -42.379 + 2.04901523*T + 10.14333127*RH - .22475541*T*RH - .00683783*T*T - .05481717*RH*RH + .00122874*T*T*RH + .00085282*T*RH*RH - .00000199*T*T*RH*RH
    else:
        T = (T*(9/5)) + 32
        index = -42.379 + 2.04901523*T + 10.14333127*RH - .22475541*T*RH - .00683783*T*T - .05481717*RH*RH + .00122874*T*T*RH + .00085282*T*RH*RH - .00000199*T*T*RH*RH
        index = (index-32.0) * (5.0/9.0)
    return index

def insertWeatherData(temperature, humidity, pressure):
    try:
        # Establish the connection
        with mysql.connector.connect(
            host="localhost",
            user="arduino_r4",    # e.g., "root"
            password="12345",
            database="weather_station"
        ) as connection:
            
            if connection.is_connected():
                with connection.cursor() as cursor:
                    index = getHeatIndex(temperature, humidity)
                    cursor.execute(f"INSERT INTO weather_data (temperature, humidity, pressure_atm, heat_index) VALUES ({temperature:.2f}, {humidity:.2f}, {pressure:.3f}, {index:.2f})")
                    connection.commit()
                    return 0

    except Error as e:
        return e

app = Flask(__name__)

logger.info("Flask server started.")

@app.route('/')
def front_page():
    return 'Weather station'

@app.route('/weather_update', methods=['POST'])
def weather_update():
    if request.method == 'POST':
        temperature = request.json['temperature']
        humidity = request.json['humidity']
        pressure_atm = request.json['pressure_atm']

        database_update_return = insertWeatherData(temperature, humidity, pressure_atm)
        if(database_update_return == 0):
            timestamp = datetime.now()
            logger.info(f"({timestamp}) Successful weather data update - Temperature={temperature}, Humidity={humidity}, Pressure={pressure_atm}")
            return {"insert_success": 1}
        else:
            logger.error(f"({timestamp}) Failed weather data update; {database_update_return}")
            return {"insert_success": 0}
    else:
        return 'Not a post request.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
