from cryptography.fernet import Fernet
from captcha_bot import captcha
import time

id = captcha()
key = Fernet.generate_key()
f = Fernet(key)

message = input("Enter a message: ").encode()

token = f.encrypt(message)

dec = f.decrypt(token)
plaintext = dec.decode('utf8')

print("Encrypting message...")
time.sleep(2)
print("Your message token is: \n %s" % id)
time.sleep(2)
print("Encrypted message: %s" % token)
time.sleep(2)
print("Decrypting message...")
time.sleep(2)
print("Message reads: %s" % plaintext)


