import time
import os
import debugGPIO as GPIO
# import RPi.GPIO as GPIO
from threading import Thread
import morse_convertor as MorseConvertor

DEBUG = 1
READ_PIN = 17
WRITE_PIN = 18
STOP_READING = 20000

GPIO.setmode(GPIO.BCM)
GPIO.setup(WRITE_PIN, GPIO.OUT)

TRESHOLD = 100
WRITE_PERIOD = 0.3
READ_PERIOD = 0.1
PERIOD = 3

# (led_enable_time, led_disable_time)
morse_chars = {
    '.': (1, 1),
    '-': (2, 1),
    '_': (0, 1),
    '/': (0, 2)
}

class Transmit(Thread):

    message = ''

    def __init__(self, message):
        Thread.__init__(self)
        self.message = message

    def transmit(self, morse_char):
        enable_time, disable_time = morse_chars[morse_char]
        GPIO.output(WRITE_PIN, True)
        time.sleep(WRITE_PERIOD * enable_time)
        GPIO.output(WRITE_PIN, False)
        time.sleep(WRITE_PERIOD * disable_time)
        GPIO.cleanup()

    def run(self):
        morse_message = MorseConvertor.encode(self.message)
        print("Start of transmit - message: \"{:s}\"".format(self.message))

        for morse_char in morse_message:
            print("Trasmitting char: \"{:s}\"".format(morse_char))
            self.transmit(morse_char)

        print("End of transmit")


class Receive(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            word = self.receiveWord()
            if not word or word == '_':
                break

            print(MorseConvertor.decode(word) + " ", end="")


    # takes about 1ms to read value
    def receiveValue(self):
        value = 0
        GPIO.setup(READ_PIN, GPIO.OUT)
        GPIO.output(READ_PIN, GPIO.LOW)
        GPIO.setup(READ_PIN, GPIO.IN)

        while (GPIO.input(READ_PIN) == GPIO.LOW):
            value += 1

            if value == STOP_READING:
                return 0

        return value

    def receiveWord(self):
        values = []
        n_zeros = 0
        slash_zeros = PERIOD * morse_chars['/'][1] + PERIOD

        while True:
            value = 1 if self.receiveValue() > TRESHOLD else 0
            values.append(value)
            
            if not value:
                n_zeros = n_zeros + 1

            if n_zeros == slash_zeros:
                return self.decodeWord(values[0:len(values)-n_zeros+PERIOD])

            time.sleep(READ_PERIOD - 0.002) # delay

    def decodeWord(self, values):
        n_ones = 0
        n_zeros = 0
        dot = [PERIOD * i for i in morse_chars['.']] 
        dash = [PERIOD * i for i in morse_chars['-']]
        underscore = [PERIOD * i for i in morse_chars['_']]
        word = ''

        for l in values:
            if l:
                n_ones = n_ones + 1
            else:
                n_zeros = n_zeros + 1

            if n_ones == dot[0] and n_zeros == dot[1]:
                word += '.'
            elif n_ones == dash[0] and n_zeros == dash[1]:
                word += '-'
            elif n_ones == underscore[0] and n_zeros == underscore[1]:
                word += '_'
            else:
                continue
            n_ones = 0
            n_zeros = 0

        return word

if __name__ == "__main__":
    transmit = Transmit("AHOJ SVETE")
    Receive = Receive()

    Receive.start()
    transmit.start()