morseAlphabet = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    " ": "/"
}

inverseMorseAlphabet = dict((v, k) for (k, v) in morseAlphabet.items())

# parse a morse code string positionInString is the starting point for decoding
def decode(code, positionInString = 0):
    if positionInString < len(code):
        morseLetter = ""
        for key,char in enumerate(code[positionInString:]):
            if char == "_":
                positionInString = key + positionInString + 1
                letter = inverseMorseAlphabet[morseLetter]
                return letter + decode(code, positionInString)
            else:
                morseLetter += char
    else:
        return ""

# encode a message in morse code, spaces between words are represented by '/'
# space between letters are represented by '_'
def encode(message):
    encodedMessage = ""
    for char in message[:]:
        encodedMessage += morseAlphabet[char.upper()] + ('_' if char != '/' else '')

    return encodedMessage