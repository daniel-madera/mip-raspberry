from Tkinter import *
import time
import colorsys
import threading

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

pwmRed = GPIO.PWM(18, 500)
pwmRed.start(100)

pwmGreen = GPIO.PWM(24, 500)
pwmGreen.start(100)

pwmBlue = GPIO.PWM(23, 500)
pwmBlue.start(100)


class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        Label(frame, text='Red').grid(row=0,column=0)
        Label(frame, text='Green').grid(row=1,column=0)
        Label(frame, text='Blue').grid(row=2,column=0)
      
        self.scaleRed = Scale(frame, from_=0, to=100, orient=HORIZONTAL, command=self.updateRed)
        self.scaleRed.grid(row=0, column=1)

        self.scaleGreen = Scale(frame, from_=0, to=100, orient=HORIZONTAL, command=self.updateGreen)
        self.scaleGreen.grid(row=1, column=1)

        self.scaleBlue = Scale(frame, from_=0, to=100, orient=HORIZONTAL, command=self.updateBlue)
        self.scaleBlue.grid(row=2, column=1)

        QUIT = Button(frame, text = 'Quit', command=self.quit)
        QUIT.grid(row=3,column=1)

    def updateRed(self, duty):
        pwmRed.ChangeDutyCycle(float(duty))

    def updateGreen(self, duty):
        pwmGreen.ChangeDutyCycle(float(duty))

    def updateBlue(self, duty):
        pwmBlue.ChangeDutyCycle(float(duty))

    def quit(self):
        root.destroy()

    def changeColor(self):
        red = self.scaleRed.get()
        green = self.scaleGreen.get()
        blue = self.scaleBlue.get()

        if red == 100:
            red = 0
            green = 100
            blue = 0
        elif green == 100:
            red = 0
            green = 0
            blue = 100
        else:
            red = 100
            green = 0
            blue = 0
            

        # hsv = list(colorsys.rgb_to_hsv(red/100, green/100, blue/100))
        # hsv[1] = 1
        # hsv[0] += 0.1
        # if hsv[0] >= 1:
        #     hsv[0] = 0
        # rgb = colorsys.hsv_to_rgb(*hsv)

        # print(hsv)

        # red = rgb[0] * 100
        # green = rgb[1] * 100
        # blue = rgb[2] * 100

        self.scaleRed.set(red)
        self.scaleGreen.set(green)
        self.scaleBlue.set(blue)

#        print(hsv)

    def demo(self):
        self.changeColor()
        t = threading.Timer(1, self.demo)
        t.start()


root = Tk()
root.wm_title =('RGB LED Control')
app = App(root)
app.scaleRed.set(100)
app.scaleGreen.set(100)
app.scaleBlue.set(100)

app.demo()
root.geometry =("200x150+0+0")
root.mainloop()
