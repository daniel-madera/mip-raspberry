import unittest
import morse
import morse_convertor

class MorseTest(unittest.TestCase):

	def testDecodeWord(self):
		receive = morse.Receive()
		values = [1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,
		1,1,1,0,0,0,1,1,1,0,0,0,0,0,0]
		expected = '.-_.._'
		actual = receive.decodeWord(values)
		self.assertEqual(actual, expected)

	def testEncode(self):
		expected = ".-_...._---_.---_/_..._...-_._-_._"
		actual = morse_convertor.encode("AHOJ SVETE")
		self.assertEqual(actual, expected)

	def testDecode(self):
		expected = "AHOJSVETE"
		actual = morse_convertor.decode(".-_...._---_.---_..._...-_._-_._")
		self.assertEqual(actual, expected)


if __name__ == '__main__':
	unittest.main()