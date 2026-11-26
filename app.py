# app.py

from flask import Flask, render_template, request, redirect, session
from mysql.connector import Error
import mysql.connector
import datetime
import logging

def getHeatIndex(T, RH, fahrenheit=False):
    index = 0
    if (fahrenheit):
        index = -42.379 + 2.04901523*T + 10.14333127*RH - .22475541*T*RH - .00683783*T*T - .05481717*RH*RH + .00122874*T*T*RH + .00085282*T*RH*RH - .00000199*T*T*RH*RH
    else:
        T = (T*(9/5)) + 32
        index = -42.379 + 2.04901523*T + 10.14333127*RH - .22475541*T*RH - .00683783*T*T - .05481717*RH*RH + .00122874*T*T*RH + .00085282*T*RH*RH - .00000199*T*T*RH*RH
        index = (T-32) * (5/9)
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
                    timestamp = datetime.now()
                    index = getHeatIndex(temperature, humidity)
                    cursor.execute(f"INSERT INTO weather_data ({timestamp}, {temperature}, {humidity}, {pressure}, {index})")
    
                    # Example: Modifying data (INSERT, UPDATE, DELETE)
                    # cursor.execute("INSERT INTO users (name) VALUES (%s)", ("Alice",))
                    # connection.commit()  # Required to save changes!
                    return 0

    except Error as e:
        print(f"MySQL error: {e}")
        return 1

app = Flask(__name__)

@app.route('/')
def view_form():
    return 'Hi!'

@app.route('/handle_post', methods=['POST'])
def handle_post():
    if request.method == 'POST':
        temperature = request.form['temperature']
        humidity = request.form['humidity']
        pressure_atm = request.form['pressure_atm']

        if(insertWeatherData(temperature, humidity, pressure_atm) == 1):
            print()
    else:
        return 'Not a post request.'

if __name__ == '__main__':
    app.run()