#!/usr/bin/python

import Tkinter


def button_clicked():
    print "Button clicked!"


def main():
    app = Tkinter.Tk()

    label = Tkinter.Label(app, text="Hello, world")
    label.pack()

    button = Tkinter.Button(app, text="Ok!", command=button_clicked)
    button.pack()

    app.mailoop()


if __name__ == '__main__':
    main()
