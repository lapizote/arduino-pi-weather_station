from mysql.connector import Error
import mysql.connector
from datetime import datetime
import logging

import requests

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
        print(f"MySQL error: {e}")
        return 1

def postRequest(url, headers, payload):
    response = requests.post(url, json=payload, timeout=10)

    if response.ok:
        print("Success:", response.json())
    else:
        print("Error:", response.status_code, response.text)

if __name__ == '__main__':
    timestamp = datetime.now()

    payload = {
        "temperature": 20.5,
        "humidity": 20.5, 
        "pressure_atm": 77.5
    }

    postRequest("http://127.0.0.1:5000/weather_update", {}, payload)


    '''if(insertWeatherData(20.2, 55.0, 1.035) == 0):
        print(f"({timestamp}) Successful weather data update - Temperature={25.0}, Humidity={55.0}, Pressure={1.035}")
    else:
        print(f"({timestamp}) Failed weather data update!")
    #print(f"{getHeatIndex(21.5, 12.0):.6f}")
    #insertWeatherData(25.0, 55.0, 1.035)'''