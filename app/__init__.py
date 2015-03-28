from flask import Flask

app = Flask(__name__)

from app import views
from app import tasks
from app import controller
from app import utilities


import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)




