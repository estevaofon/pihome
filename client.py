#!/usr/bin/python
import RPi.GPIO as GPIO
import requests
import json
import time
import logging

logging.basicConfig(filename='client.log',level=logging.WARNING,
        format='%(asctime)s - %(levelname)s - %(message)s')

GPIO.setmode(GPIO.BCM)
pins = {
    24: {'name': 'Ventilador', 'state': GPIO.LOW},
    23: {'name': 'Lâmpada', 'state': GPIO.LOW}
    }

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def loop():
    while 1:
        global pins
        try:
            response = requests.get("http://localhost:5000/api")
            pins = json.loads(response.text)
        except requests.exceptions.RequestException as e:
            logging.exception("Request exception happened")

        for pin in pins:
            state = pins[pin]['state']
            if state == '0' and GPIO.input(int(pin)) == 0:
                pass
            if state == '1' and GPIO.input(int(pin)) == 1:
                pass
            if state == '1' and GPIO.input(int(pin)) == 1:
                GPIO.output(int(pin), GPIO.LOW)
                print("Acendeu")
            if state == '0' and GPIO.input(int(pin)) == 0:
                GPIO.output(int(pin), GPIO.HIGH)
                print("Apagou")
        time.sleep(2)
try:
    loop()
except:
    logging.exception("Error message")
finally:
    GPIO.cleanup()
    print("Closed Everything.")
