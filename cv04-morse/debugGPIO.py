BCM = 1
OUT = 0
LOW = 1
IN = 1

def setmode(*args):
	_print('GPIO.setmode', *args)

def setup(*args):
	_print('GPIO.setup', *args)

def output(*args):
	_print('GPIO.output', *args)

def input(*args):
	_print('GPIO.input', *args)

def cleanup(*args):
	_print('GPIO.cleanup', *args)

def _print(name, *args):
	args = [str(a) for a in args]
	print("{:s}({:s})".format(name, ', '.join(args)))