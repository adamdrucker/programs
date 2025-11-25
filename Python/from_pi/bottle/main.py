from bottle import route, run, post, get, request, template, error, static_file
from cryptography.fernet import Fernet
from Crypto import Cipher
from captcha_bot import captcha
from crypt import *
import pyperclip as pc
import os


''' The captcha_bot module imports a small program that generates a string of six pseudo-random
    characters that is only used in the URL for the encrypted method.

    Fernet encryption is used via the cryptography module for Python.

    AES and Blowfish are used via the Crypto module for Python.

    Pyperclip is a module used to enable the copy button on the encryption page.

'''

# List to append the 'url' value to, this will be checked later on
# If the URL generated during encryption exists in the list, the message can be decrypted
# If it does not, the message will not be displayed
approved_list = []


# Entry page - 'http://localhost:8080/message'
@route('/message')
def message_in():    

    algorithms = ['AES', 'Blowfish' , 'Fernet']
    
    # Brief descriptions for the algorithms, displayed on entry page
    alg_desc = [' is a federally approved encryption algorithm. It has been adopted by agencies such as the NSA for top secret information.',
    ' is a general-purpose encryption algorithm. It works well with short messages.',
    ' encryption makes use of 128-bit AES encryption, and is a good choice when working with the Python language.']

    # Items for drop down list
    variables = {"algorithms": algorithms, "alg_desc": alg_desc}

    # Returns the input form prior to encryption
    return template("form.html", variables)



# Page displayed after encryption
@post('/encrypted')
def do_encrypt():

    # Function to enable copy button
    def copyFunc(link):
        pc.copy(link)

    # Input taken from user, encoded for encryption
    message = request.forms.get('message').encode()

    # This generates a randomized path for the URL for each message encrypted
    url = captcha()
    approved_list.append(url)
    link = "localhost:8080/message/{url}".format(url=url)

    # Enabled the copy button to grab the URL
    pc_url = pc.copy(link)

    
    # Encrypt functions below
    # // 'message' passed as argument
    # Not ideal using globals, but it works for the time being
    global e_method
    global aes_plain
    global blowfish_plain
    global fernet_plain

    # This successfully displays the encryption method selected from the dropdown
    e_method = request.forms.get('enc')

    # The "[encryption-name]_cipher" variables contain the encrypted message,
    # but are currently not displayed anywhere
    if e_method == 'AES':
        aes_cipher, aes_plain = aes_encrypt(message)
    elif e_method == 'Blowfish':
        blowfish_cipher, blowfish_plain = blowfish_encrypt(message)
    elif e_method == 'Fernet':
        fernet_cipher, fernet_plain = fernet_encrypt(message)


    # Variables passed into HTML
    variables = {"link": link, "url": url, "pc_url": pc_url, "e_method": e_method}

    return template("encryption_page.html", variables)


# Page displayed after decryption
@get('/message/<url>')
def show_message(url):

    
    # Decrypt functions
    if url in approved_list:
        if e_method == 'AES':
            plaintext = aes_plain
        elif e_method == 'Blowfish':
            plaintext = blowfish_plain
        elif e_method == 'Fernet':
            plaintext = fernet_plain

        approved_list.pop()
    else:
        plaintext = 'Message not available'
        


    # Vars passed into HTML
    variables = {"message": plaintext}
    
    return template("decryption_page.html", variables)






if __name__ == '__main__':
    run(host="localhost", port=8080, debug=True, reloader=True)
