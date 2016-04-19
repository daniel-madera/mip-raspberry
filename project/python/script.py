import webiopi
import json

GPIO = webiopi.GPIO

L1 = 14
L2 = 18
L3 = 25
L4 = 8
L5 = 2
L6 = 4
L7 = 17

B1 = 15
B2 = 23
B3 = 24
B4 = 7
B5 = 3
B6 = 27
B7 = 22


def setup():
    # set as output
    GPIO.setFunction(L1, GPIO.OUT)
    GPIO.setFunction(L2, GPIO.OUT)
    GPIO.setFunction(L3, GPIO.OUT)
    GPIO.setFunction(L4, GPIO.OUT)
    GPIO.setFunction(L5, GPIO.OUT)
    GPIO.setFunction(L6, GPIO.OUT)
    GPIO.setFunction(L7, GPIO.OUT)

    # set as input
    GPIO.setFunction(B1, GPIO.OUT)
    GPIO.setFunction(B2, GPIO.OUT)
    GPIO.setFunction(B3, GPIO.OUT)
    GPIO.setFunction(B4, GPIO.OUT)
    GPIO.setFunction(B5, GPIO.OUT)
    GPIO.setFunction(B6, GPIO.OUT)
    GPIO.setFunction(B7, GPIO.OUT)


def loop():
    # logic for hw handlers buttons goes here
    pass


def destroy():
    # turn off LEDS
    GPIO.digitalWrite(L1, GPIO.LOW)
    GPIO.digitalWrite(L2, GPIO.LOW)
    GPIO.digitalWrite(L3, GPIO.LOW)
    GPIO.digitalWrite(L4, GPIO.LOW)
    GPIO.digitalWrite(L5, GPIO.LOW)
    GPIO.digitalWrite(L6, GPIO.LOW)
    GPIO.digitalWrite(L7, GPIO.LOW)


@webiopi.macro
def b1_clicked():
    GPIO.digitalWrite(L1, GPIO.HIGH)
    return status()


@webiopi.macro
def status():
    stat = dict(L1=GPIO.digitalRead(L1), L2=GPIO.digitalRead(L2),
                L3=GPIO.digitalRead(L3), L4=GPIO.digitalRead(L4),
                L5=GPIO.digitalRead(L5), L6=GPIO.digitalRead(L6),
                L7=GPIO.digitalRead(L7))
    return json.dumps(stat)
