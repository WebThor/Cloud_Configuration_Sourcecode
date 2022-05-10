from abc import ABC
import os
from logging import basicConfig
import random
from Crypto.Cipher import AES
import contract
import blockchainFunctions
import json
from base64 import b64decode, b64encode
from Crypto.Cipher import AES
import time
from dotenv import load_dotenv





   
def keyManagementFlow(w3,contract_instance, blockchainAddress, keyConsumer, g, p):
    b =  int(random.random() *100000)
        
    #Set Value B
    B = g ** b % p

    blockchainFunctions.setValueOne(w3,contract_instance,blockchainAddress,B,keyConsumer)


    #Get Value for CloudConsumer
    A = blockchainFunctions.getValueOne(contract_instance,keyConsumer)

        
    AB = A ** b % p

    #Set Value AB
    blockchainFunctions.setValueTwo(w3,contract_instance,blockchainAddress,AB,keyConsumer)

    #let other party set second Diffie Hellman value
    time.sleep(10)

    #Get Value for CloudConsumer
    CA = blockchainFunctions.getValueTwo(contract_instance,keyConsumer)

    return CA ** b % p
        
        

def encryptMessage(skey,m):
    skey = skey.to_bytes(16,'big')
    header = b"header"
        
    cip = AES.new(skey, AES.MODE_GCM)
    cip.update(header)

    c, t = cip.encrypt_and_digest(m)
    return c,t
        
def decryptMessage(skey, c, t):
    skey = skey.to_bytes(16,'big')
    header = b"header"
    cip = AES.new(skey, AES.MODE_GCM)
    cip.update(header)


    decipher = AES.new(skey, AES.MODE_GCM, nonce=cip.nonce)
    decipher.update(header)
    plaintext = decipher.decrypt_and_verify(c,t)
    return plaintext


