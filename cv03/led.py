import time
import colorsys
import threading

import RPi.GPIO as GPIO
import time
import os
     
DEBUG = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.IN)


led = GPIO.output(17, True)


def RCtime (RCpin):
    reading = 0
    GPIO.setup(RCpin, GPIO.OUT)
    GPIO.output(RCpin, GPIO.LOW)
    time.sleep(0.1)
            
    GPIO.setup(RCpin, GPIO.IN)
    # This takes about 1 millisecond per loop cycle
    while (GPIO.input(RCpin) == GPIO.LOW):
        reading += 1
    return reading


def main():
    while True:
        print RCtime(18)


if __name__ == '__main__':
    main()
