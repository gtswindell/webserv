from app import app
from flask import Flask, jsonify, request
from datetime import datetime

import RPi.GPIO as GPIO
import Adafruit_DHT

import sqlite3 as lite
import sys


ledPin = 25
dht22 = 4

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(ledPin, GPIO.OUT)


@app.route('/controller/api/v1.0/led', methods=['GET'])
def ledStatus():
    state = GPIO.input(ledPin)
    return jsonify({'led state': state})


@app.route('/controller/api/v1.0/led/<int:led_state>', methods=['GET'])
def switchLed(led_state):
    GPIO.output(ledPin, led_state)
    return ledStatus()

@app.route('/controller/api/v1.0/temperature', methods=['POST'])
def setTemperature():
        area = request.json['area']
        temperature = request.json['temperature']
	humidity = request.json['humidity']
	con = lite.connect('/home/glen/projects/webserv/app/data/temps.dat')

	with con:
		try:
			cur = con.cursor()
			cur.execute("INSERT INTO temperature VALUES (?, ?, ?, ?)", (area, datetime.now(), temperature, humidity))
			con.commit()
			return jsonify({'state':'ok'})
		except Exception as inst:
			con.rollback()
			return jsonify({'exception': inst})
	con.close()

@app.route('/controller/api/v1.0/temperature/<int:area>', methods=['GET'])
def getTemperature(area):
	#try:
	#	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, area)
	#	if ((humidity <> None) and (temperature <> None)):
	#		return jsonify({'humidity': '{0:0.1f}'.format(humidity), 'temperature': '{0:0.1f}'.format(temperature)})
	#	else:
	#		return jsonify({'error': 'No data returned'})
	#except RuntimeError:
	#	type, value, traceback = sys.exc_info()
	#	return jsonify({'Error': value.strerror})
    con = lite.connect('/home/glen/projects/webserv/app/data/temps.dat')
    with con:
        try:
            cur = con.cursor()
            cur.execute("SELECT temp, humidity from temperature where station = ? order by dt DESC", (area,))
            row = cur.fetchone()
            if row is not None:
                humidity = row[1]
                temp = row[0]
                return jsonify({'station': area, 'humidity': humidity, 'temperature': temp})
            else:
                return  jsonify({'error': 'No data returned'})
        except RuntimeError:
            type, value, traceback = sys.exc_info()
            return jsonify({'Error': value.strerror})
         
