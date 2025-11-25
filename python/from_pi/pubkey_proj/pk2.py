import random
import os
from random import seed

#ALPHABET = "abcdefghijklmnopqrstuvwxyz"

#for position, character in enumerate(ALPHABET):
#    print(ALPHABET.index(character), character.upper())




'''
random.seed(os.urandom(random.randint(234, 978)))

for i in range(10):
    print(random.randint(1, 10000))
'''
# Line break
# print("-"*8)

# Prints two identical blocks of random floats
'''
for i in range(2):
    random.seed(10)
    for i in range(20):
        print(random.random())
    print()
'''

# Line break
# print("-"*8)
'''
random.seed(1)
for i in range(5):
    print(random.random())
'''

seed(random.randint(0, 255))

r = random.randint(random.randint(0 ,511), random.randint(512, 1023))
print(r)

def r_seed(x, y):
    x = round(x * 1.986 / 15 + (random.randint(43, 157)))
    y = round(y + 43 * 0.1516 - (random.randint(177, 434)))

    if x < 0:
        x = x * -1

    if y < 0:
        y = y * -1

    if x > y:
        x = round(x * 0.25)

    return x, y

testing = (r_seed(r, r))
a = testing[0]
b = testing[1]
print(r_seed(r, r))
print(random.randint(a, b))

'''
def r_seed(x, y):
    x = round(x * 0.1516 + 15 - (random.randint(43, 157)))
    y = round(y - 43 * 1.986 + (random.randint(177, 434)))

    if x < 0:
        x = x * -1

    if y < 0:
        y = y * -1

    if x > y:
        return x, y
    else:
        return y, x
'''

    

