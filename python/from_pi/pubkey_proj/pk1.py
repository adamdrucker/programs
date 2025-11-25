from caesar import caesar

# private key pairs
privatekey = [ [2, 5], [7, 11], [13, 17], [19, 23] ]

# Encrypt or decrypt?
encrypt = input("Encrypting or decrypting? [E/D]: ").upper()
if encrypt == "E":
    encrypting = True
elif encrypt == "D":
    encrypting = False
else:
    print("Must be E or D, cannot continue")
    exit(0)

# Which set of keys should be used?
print("Choice of keys is as follows: ")
for i in range(len(privatekey)):
    print("Private key set %s is [%s, %s] (public key %s)" % (i, privatekey[i][0], privatekey[i][1], privatekey[i][0] * privatekey[i][1]))
keyindex = int(input("Which set of keys? (0-3): "))
if keyindex > 3:
    print("Keys must be in range (0-3)")
    exit(0)

# Find out if private key A or B should be used
user = input("Which user - Alice or Bob? (A/B): ").upper()
if user == "A":
    username = "Alice"
    # Alice's pk choice from selected set depends on whether she is encrypting or decrypting
    if encrypting:
        useridx = 0
    else:
        useridx = 1
elif user == "B":
    username = "Bob"
    # Bob's pk choice from selected set depends on whether he is encrypting or decrypting
    if encrypting:
        useridx = 1
    else:
        useridx = 0
else:
    print("User must be A or B, cannot proceed.")
    exit(0)

# What plaintext should be encrypted
msgtext = input("Message text to be processed using cipher: ")
msgtext = msgtext.replace(" ", "X") # Replace spaces with X
msgtext = msgtext.upper()           # Force all characters to upper case

# Public key is the product of the pair of private keys
publickey = privatekey[keyindex][0] * privatekey[keyindex][1]

# Obtain Caesar cipher using the selected private key
if encrypting == True:
    ciphertext = caesar(msgtext, privatekey[keyindex][useridx])
else:
    plaintext = caesar(msgtext, -privatekey[keyindex][useridx])

if encrypting == True:
    print("%s therefore sends public key %s and %s as ciphertext %s" % (username, publickey, msgtext, ciphertext))
else:
    print("%s therefore decrypts %s as %s" % (username, msgtext, plaintext))
