#!/usr/bin/env python3
# (c) 2021 Rick Sanchez
import pathlib, os
from conf.config import *
from cryptography.fernet import Fernet


def sessionID(WorkPath):
    filename = pathlib.Path(WorkPath+'/auth.bin')
    if filename.is_file():
        keyID=filename.read_text()
        return keyID
    else:
        authKey=Fernet.generate_key()
        with open(WorkPath+'/auth.bin', 'wb') as file_object:  file_object.write(authKey)
        return authKey

def decrypt(sessionID, passw, WorkPath):
    if passw =='':
        return ''

    if passw =='###':
        filename = pathlib.Path(WorkPath+'/sppwd.bin')
        if filename.is_file():
            with open(WorkPath+'/sppwd.bin', 'rb') as file_object:
                for line in file_object:
                    encryptedpwd = line
        cipher_suite = Fernet(sessionID)
        ciphered_text= encryptedpwd
        unciphered_text = (cipher_suite.decrypt(ciphered_text))
        plain_text_encryptedpassword = bytes(unciphered_text).decode("utf-8")
        return plain_text_encryptedpassword


def encrypt(sessionID, pwd, WorkPath):
    cipher_suite = Fernet(sessionID)
    ciphered_text = cipher_suite.encrypt(pwd.encode())   #required to be bytes
    with open(WorkPath+'/sppwd.bin', 'wb') as file_object:  file_object.write(ciphered_text)
    return "###"

#Function for saving Config
def writestuff(keyID, WorkPath, hostname, p, usrname, pwd, k):
    if not pwd == '':
        passw=encrypt(keyID, pwd, WorkPath)
    else:
        passw=''
    f = open(WorkPath+'/config.py',"w")
    configcontent ="#!/usr/bin/env python3\nhostname='"+hostname+"'\np='"+p+"'\nusrname='"+usrname+"'\npassw='"+passw+"'\nk='"+k+"'\n"
    f.write(configcontent)


#Session Handler
WPath=os.path.dirname(os.path.realpath(__file__))
keyID = sessionID(WPath)
passwd =  decrypt(keyID, passw, WPath)
