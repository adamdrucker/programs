from Crypto.Cipher import Blowfish
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto import Random
from cryptography.fernet import Fernet
from random import randint
from random import seed
import cryptography
import random
import time
import os


''' This library contains two parts to it; the first is the encryption sequence I created based on
    a Caeser cipher tutorial with some modifications. This requires the generation and usage of a
    One-Time Pad text file. This works fine, except it relies on two text files being stored and
    loaded/deleted.

    The second portion contains crypto functions from the Python module PyCrypto. These are well-known
    algorithms such as AES. All cryptographic functions will be kept in this module and then imported
    into the main Bottle project file.

    This includes an MD5 hashing function - this won't be used on the Bottle project to encrypt
    messages (obviously) but is still being included in case there is future use.

'''

# // START Legacy encryption code //

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
ALPHAUP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PUNC = ",.:;!?@#$%^&*-_`~/\[]{}()<>'\""   # 29 length

# Seed to init random generator
seed(random.randint(random.randint(0, 255), (random.randint(256, 511))))

# Generate two random numbers to be used in the OTP randomization
r = random.randint(random.randint(0, 251), random.randint(257, 509))
s = random.randint(random.randint(521, 1021), random.randint(1031, 2039))

# Create one-time pad with randomized numbers
def generate_otp(length):
        with open("otp.txt", "w") as f:
            for i in range(length):
                f.write(str(random.randint(r, s)) + "\n")


# // File functions //
# ///////////////////
def load_sheet(filename):
    with open(filename, "r") as f:
        contents = f.read().splitlines()
    return contents

def get_plaintext():
    plain_text = input("Please type your message: ")
    return plain_text

def load_file(filename):
    with open(filename, "r") as f:
        contents = f.read()
    return contents

def save_file(filename, data):
    with open(filename, "w") as f:
        f.write(data)



# // Encryption //
# ///////////////

''' This function takes in a plaintext message and an OTP sheet from 
    the ones generated in the first function. Any characters not in
    the ALPHABET/ALPHAUP/PUNC variables are added as-is to the CIPHERTEXT variable.
    The ENCRYPTED value is derived from the index of each character in the ALPHABET
    plus the value in the 0-based corresponding position of the OTP text file.
    This is then modulus divided by the length of the string and the corresponding
    character at the index position is chosen as the ciphertext character.
'''

def encrypt(plaintext, sheet):
    ciphertext = ''
    for position, character in enumerate(plaintext):      
        if character in ALPHABET:
            encrypted = (ALPHABET.index(character) + int(sheet[position])) % 26
            ciphertext += ALPHABET[encrypted]
        elif character in ALPHAUP:
            encrypted = (ALPHAUP.index(character) + int(sheet[position])) % 26
            ciphertext += ALPHAUP[encrypted]
        elif character in PUNC:
            encrypted = (PUNC.index(character) + int(sheet[position])) % 29
            ciphertext += PUNC[encrypted]
        else:
            ciphertext += character
            
            # // The following print statements can be used to see what's happening
            # // inside this encrypt function
            
            #print("Alphabet index char is: ", ALPHABET.index(character))
            #print("Sheet pos is: ", int(sheet[position]))
            #print("Value of encrypted is: ", encrypted)
            
    return ciphertext


# // Decryption //
# ///////////////

''' Essentially the same operation as above, except characters in the CIPHERTEXT
    message are being applied to the PLAINTEXT variable, and index/sheet positions
    are subtracted from one another rather than added.
'''

def decrypt(ciphertext, sheet):
    plaintext = ''
    for position, character in enumerate(ciphertext):
        if character in ALPHABET:
            decrypted = (ALPHABET.index(character) - int(sheet[position])) % 26
            plaintext += ALPHABET[decrypted]
        elif character in ALPHAUP:
            decrypted = (ALPHAUP.index(character) - int(sheet[position])) % 26
            plaintext += ALPHAUP[decrypted]
        elif character in PUNC:
            decrypted = (PUNC.index(character) - int(sheet[position])) % 29
            plaintext += PUNC[decrypted]
        else:
            plaintext += character
    return plaintext

# // END Legacy encryption code //


''' For certain block cipher encryption modes, the plaintext messages have
    to be a multiple of the block size for each algorithm. To ensure that each
    of these functions will perform the prescribed encryption on data of any length,
    padding may be required for certain modes.

    CFB mode, described in a comment under the AES section, turns the block cipher
    into a steam cipher and eliminates the requirement of plaintext to be a multiple
    in length of the block size, nor does it require padding on the plaintext input.
'''

# // MD5 Hashing //
# ////////////////

def md5_hash(plaintext):


        ''' https://en.wikipedia.org/wiki/MD5 '''
                
    
        # Create a new instance of the hash object
        hash = MD5.new()
    
        # Encode a message for hashing
        message = plaintext.encode()
    
        # The 'update' method continues the hashing by consuming the next chunk
        hash.update(message)
    
        # The 'digest' method returns a digest of what's been hashed so far
        digest = hash.digest()
    
        return digest
    

# // AES Encryption //
# ///////////////////

def aes_encrypt(plaintext):

    ''' https://en.wikipedia.org/wiki/Advanced_Encryption_Standard '''
        
    # Create new AES cipher
    # An IV can be used, but 'MODE_ECB' ignores it
    iv = Random.new().read(AES.block_size)
    
    # AES.MODE_CFB seems to mitigate the issue with input/plaintext length
    # CFB is "Cipher FeedBack" - this turns the block cipher into a stream cipher
    obj = AES.new('This is a key456This is a key456',AES.MODE_CFB, iv)
    
    message = plaintext
    
    ciphertext = obj.encrypt(message)
       
    # This decrypts and decodes
    # Per pypi.org documentation,a second object is needed in order
    # to properly decrypt
    obj2 = AES.new('This is a key456This is a key456',AES.MODE_CFB, iv)
    
    # The decode() method below converts from byte string to UTF8
    aes_decrypt = obj2.decrypt(ciphertext).decode('utf-8')
    
    return ciphertext, aes_decrypt  # Returns both as a tuple, must be unpacked when called


# // Blowfish Encryption //
# ////////////////////////

def blowfish_encrypt(plaintext):

    ''' https://en.wikipedia.org/wiki/Blowfish_(cipher) '''
    
    bs = Blowfish.block_size    # 8 bits
    
    key = "An arbitrarily long key"
    
    iv = Random.new().read(bs)
    
    # CFB mode works identical to the AES change made above
    # This appears to allow for plaintext input of any length
    obj = Blowfish.new(key, Blowfish.MODE_CFB, iv)
    
    message = plaintext  # Removed .decode() from here to make it work in the Bottle site
    
    ciphertext = obj.encrypt(message)
    
    # A new object is required for decryption (similar to AES)
    obj2 = Blowfish.new(key, Blowfish.MODE_CFB, iv)
    blowfish_decrypt = obj2.decrypt(ciphertext).decode('utf-8')
    #plaintext = dec.decode()

    return ciphertext, blowfish_decrypt  # Returns both as a tuple, must be unpacked when called


# // Fernet Encryption //
# //////////////////////

''' Fernet symmetric encryption can be found at:
    https://cryptography.io/en/latest/fernet/
'''

def fernet_encrypt(plaintext):
    
    # Encrypt with cryptography.fernet
    # Generate a key
    key = Fernet.generate_key()
    f = Fernet(key)
    
    message = plaintext  # Removed .encode() from here to make it work in the Bottle site
    
    ciphertext = f.encrypt(message)
        
    dec = f.decrypt(ciphertext)
    fernet_decrypt = dec.decode('utf8')
    
    return ciphertext, fernet_decrypt  # Returns both as a tuple, must be unpacked when called
    

    



















