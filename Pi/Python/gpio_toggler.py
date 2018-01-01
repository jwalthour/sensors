import time, math
import RPi.GPIO as GPIO

PIN=4

def set(value):
	if value:
		GPIO.output(PIN, GPIO.HIGH)
	else:
		GPIO.output(PIN, GPIO.LOW)

	
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)
