import webiopi
import json
import RPi.GPIO

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


pwmL5 = None
duties = [0, 25, 100]
iduty = 0


def setup():
    global pwmL5
    global iduty
    
    # set as output
    GPIO.setFunction(L1, GPIO.OUT)
    GPIO.setFunction(L2, GPIO.OUT)
    GPIO.setFunction(L3, GPIO.OUT)
    GPIO.setFunction(L4, GPIO.OUT)
    # GPIO.setFunction(L5, GPIO.OUT)
    GPIO.setFunction(L6, GPIO.OUT)
    GPIO.setFunction(L7, GPIO.OUT)

    RPi.GPIO.setmode(RPi.GPIO.BCM)

    # setup buttons
    RPi.GPIO.setup(B1, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
    RPi.GPIO.setup(B2, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
    RPi.GPIO.setup(B3, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
    RPi.GPIO.setup(B4, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
    RPi.GPIO.setup(B5, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
    RPi.GPIO.setup(B6, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
    RPi.GPIO.setup(B7, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)

    # add button callbacks
    RPi.GPIO.add_event_detect(B1, RPi.GPIO.FALLING, callback=btn_callback, bouncetime=500)
    RPi.GPIO.add_event_detect(B2, RPi.GPIO.FALLING, callback=btn_callback, bouncetime=500)
    RPi.GPIO.add_event_detect(B3, RPi.GPIO.FALLING, callback=btn_callback, bouncetime=500)
    RPi.GPIO.add_event_detect(B4, RPi.GPIO.FALLING, callback=btn_callback, bouncetime=500)
    RPi.GPIO.add_event_detect(B5, RPi.GPIO.FALLING, callback=btn_callback, bouncetime=500)
    RPi.GPIO.add_event_detect(B6, RPi.GPIO.FALLING, callback=btn_callback, bouncetime=500)
    RPi.GPIO.add_event_detect(B7, RPi.GPIO.FALLING, callback=btn_callback, bouncetime=500)

    # led pwm
    RPi.GPIO.setup(L5, RPi.GPIO.OUT)
    pwmL5 = RPi.GPIO.PWM(L5, 50)
    iduty = 0
    pwmL5.start(duties[iduty])
    

def loop():
    # logic for hw handlers buttons goes here
    #pwmL5.ChangeDutyCycle(50)
    
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

    pwmL5.stop()

    RPi.GPIO.cleanup()


def toggle_led(pin):
    value = GPIO.LOW
    state = GPIO.digitalRead(pin)
    if not state:
        value = GPIO.HIGH
    GPIO.digitalWrite(pin, value)


@webiopi.macro
def b1_clicked(*args):
    toggle_led(L1)


@webiopi.macro
def b2_clicked():
    toggle_led(L2)


@webiopi.macro
def b3_clicked():
    toggle_led(L2)


@webiopi.macro
def b4_clicked():
    toggle_led(L3)
    toggle_led(L4)


@webiopi.macro
def b5_clicked():
    # toggle_led(L5)
    global iduty
    iduty = (iduty + 1) % len(duties)
    pwmL5.ChangeDutyCycle(duties[iduty])


@webiopi.macro
def b6_clicked():
    toggle_led(L6)
    stateL6 = GPIO.digitalRead(L6)
    stateL7 = GPIO.digitalRead(L7)
    if not stateL6 and stateL7:
        toggle_led(L7)


@webiopi.macro
def b7_clicked():
    toggle_led(L7)


@webiopi.macro
def status():
    stat = dict(L1=GPIO.digitalRead(L1), L2=GPIO.digitalRead(L2),
                L3=GPIO.digitalRead(L3), L4=GPIO.digitalRead(L4),
                L5=GPIO.digitalRead(L5), L6=GPIO.digitalRead(L6),
                L7=GPIO.digitalRead(L7))
    return json.dumps(stat)


BUTTON_FUNCTION_MAP = {
    B1: b1_clicked,
    B2: b2_clicked,
    B3: b3_clicked,
    B4: b4_clicked,
    B5: b5_clicked,
    B6: b6_clicked,
    B7: b7_clicked
}


def btn_callback(pin):
    if pin in BUTTON_FUNCTION_MAP:
        BUTTON_FUNCTION_MAP[pin]()

