import time
import cryptography
from cryptography.fernet import Fernet
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Cipher import Blowfish
from Crypto.Hash import MD5


''' For certain block cipher encryption modes, the plaintext messages have
    to be a multiple of the block size for each algorithm. To ensure that each
    of these functions will perform the prescribed encryption on data of any length,
    padding may be required for certain modes.

    CFB mode, described in a comment under the AES section, turns the block cipher
    into a steam cipher and eliminates the requirement of plaintext to be a multiple
    in length of the block size, nor does it require padding on the plaintext input.
'''


def decorate():
    print("=" * 34)

# -----------

def md5_hash():
    
    # Create a new instance of the hash object
    hash = MD5.new()
    
    # Encode a message for hashing
    message = "Hashing".encode()
    
    # The 'update' method continues the hashing by consuming the next chunk
    hash.update(message)
    
    # The 'digest' method returns a digest of what's been hashed so far
    digest = hash.digest()
    
    print("MD5 digest: %s" % digest)
    
    decorate()  # Spacing for test output
    
md5_hash()

# -----------

def aes_encrypt():
    # Create new AES cipher
    # An IV can be used, but 'MODE_ECB' ignores it
    iv = Random.new().read(AES.block_size)
    # AES.MODE_CFB seems to mitigate the issue with input/plaintext length
    # CFB is "Cipher FeedBack" - this turns the block cipher into a stream cipher
    obj = AES.new('This is a key456This is a key456',AES.MODE_CFB, iv)
    
    message = "Testing a string of an arbitrary length"
    
    ciphertext = obj.encrypt(message)
    
    print("AES encryption: %s" % ciphertext)
    time.sleep(1)
    print("Decrypting AES...")
    time.sleep(1)
    
    # This decrypts and decodes
    # Per pypi.org documentation,a second object is needed in order
    # to properly decrypt
    obj2 = AES.new('This is a key456This is a key456',AES.MODE_CFB, iv)
    
    # The decode() method below converts from byte string to UTF8
    aes_decrypt = obj2.decrypt(ciphertext).decode('utf-8')
    
    print(aes_decrypt)
    
    decorate()  # Spacing for test output
    
aes_encrypt()

# -----------

def blowfish_encrypt():
    
    # This prints a Blowfish encrypted message
    
    bs = Blowfish.block_size    # 8 bits
    
    key = "An arbitrarily long key"
    
    iv = Random.new().read(bs)
    # CFB mode works identical to the AES change made above
    # This appears to allow for plaintext input of any length
    obj = Blowfish.new(key, Blowfish.MODE_CFB, iv)
    
    message = b"What the hell is going on"
    
    ciphertext = obj.encrypt(message)
    
    print("Blowfish encryption: %s" % ciphertext)
    time.sleep(1)
    print("Decrypting Blowfish...")
    time.sleep(1)
    
    # A new object is required for decryption (similar to AES)
    obj2 = Blowfish.new(key, Blowfish.MODE_CFB, iv)
    dec = obj2.decrypt(ciphertext).decode('utf-8')
    #plaintext = dec.decode()

    print(dec)
    
    decorate()  # Spacing for test output
    
blowfish_encrypt()

# -----------

# This works fine for in/out crypto
def fernet_encryption():
    
    # Encrypt with cryptography.fernet
    # Generate a key
    key = Fernet.generate_key()
    f = Fernet(key)
    
    message = b"Foo foo barbar"
    
    token = f.encrypt(message)
    
    print("Fernet encryption: %s" % token)
    time.sleep(1)
    print("Decrypting Fernet...")
    time.sleep(1)
    
    dec = f.decrypt(token)
    plaintext = dec.decode('utf8')
    
    print(plaintext)
    
    decorate()  # Spacing for test output
    
fernet_encryption()



    
