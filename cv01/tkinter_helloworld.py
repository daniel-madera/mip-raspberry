#!/usr/bin/python

import Tkinter


def main():
    app = Tkinter.Tk()

    label = Tkinter.Label(app, text="Hello, world")
    label.pack()

    app.mailoop()


if __name__ == '__main__':
    main()
