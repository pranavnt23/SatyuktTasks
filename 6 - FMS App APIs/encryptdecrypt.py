# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 16:34:00 2025

@author: prana
"""

from Crypto.Cipher import AES
import base64

def encrypt(userid,pnumber,time):
    msg_text = (userid+"_"+pnumber+"_"+time).rjust(32).encode("utf8")
    secret_key = b'12123569723567455667123a' 
    cipher = AES.new(secret_key,AES.MODE_ECB)
    encoded = base64.urlsafe_b64encode(cipher.encrypt(msg_text))
    row_form = encoded.decode("utf-8")
    return row_form
    #print(row_form)
    #print(encoded)
    #print(type(encoded))
    #return str(encoded).rstrip("=")

    

def decrypt_info(key):
    print("decryption started")
    secret_key = b'12123569723567455667123a' 
    cipher = AES.new(secret_key,AES.MODE_ECB)
    print(cipher)
    #print(key)
    #key = str(key)
    #key = key[2:len(key)-2]
    padding = len(key) % 16
    key = key + ("=" * padding)
    #print(key)
    decoded = cipher.decrypt(base64.urlsafe_b64decode(key))
   # print("\n",decoded)
    info_arr = str(decoded.decode()).strip().split("_")
    return info_arr



def dec_key(e_key):
    print("decryption started")
    secret_key = b'12123569723567455667123a' 
    cipher = AES.new(secret_key,AES.MODE_ECB)
    print(cipher)
    print(e_key)
    #key = str(key)
    #key = key[2:len(key)-2]
    padding = len(e_key) % 16
    e_key = e_key + ("=" * padding)
    print(e_key)
    decoded = cipher.decrypt(base64.urlsafe_b64decode(e_key))
    if decoded == b'BnYpe57iVsB-zAWJ1i78GZzJqEyuv2BH':
        return 1
    else:
        return 0

"""en=encrypt(str(5),str(6203707621),str(454545))
print(en)
#de = decrypt_info("AFE-OSzggvelRINEfV35LOlLhPcAKObOLbgZ3FA1BAI=")
#print("bghgb: ",de)
"""
de = decrypt_info("m_kcapM9mLO-DnP1OhokNFRscADpKfctT1-E3-LrZSM=")
print("bghgb: ",de)
print(type(de))