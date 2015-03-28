from app import app
from flask import Flask, jsonify

import RPi.GPIO as GPIO
import Adafruit_DHT

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

@app.route('/controller/api/v1.0/temperature/<int:area>', methods=['GET'])
def getTemperature(area):
	try:
		humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, area)
		if ((humidity <> None) and (temperature <> None)):
			return jsonify({'humidity': '{0:0.1f}'.format(humidity), 'temperature': '{0:0.1f}'.format(temperature)})
		else:
			return jsonify({'error': 'No data returned'})
	except RuntimeError:
		type, value, traceback = sys.exc_info()
		return jsonify({'Error': value.strerror})
