import random
import os
from random import seed

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
ALPHAUP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PUNC = ",.:;!?@#$%^&*-_`~/\[]{}()<>'\""   # 29 length

inp = input("Enter a message: ")

ciphertext = ''
for character in inp:
    if character in ALPHABET:
        encrypted = (ALPHABET.index(character) + 5) % 26
        ciphertext += ALPHABET[encrypted]
    elif character in ALPHAUP:
        encrypted = (ALPHAUP.index(character) + 5) % 26
        ciphertext += ALPHAUP[encrypted]
    elif character in PUNC:
        encrypted = (PUNC.index(character) + 5) % 29
        ciphertext += PUNC[encrypted]
    else:
        ciphertext += character

    


print(ciphertext)

