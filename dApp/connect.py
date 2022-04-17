from abc import ABC
import os
from logging import basicConfig
from Crypto.Random import get_random_bytes
from eth_typing.encoding import HexStr
from web3 import Web3
from web3.auto import w3
from eth_keys import keys
from eth_account.messages import encode_defunct
import random
from Crypto.Cipher import AES
import contract
from eth_account import Account
import json
from base64 import b64decode, b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import time
from dotenv import load_dotenv

def getSymmetricParameters(contract_instance,key):
    return  contract_instance.functions.getSymmetricParameters().call({'from': Account.from_key(key).address, 'gas': 100000})


def setValueOne(w3, contract_instance, address, value, key):
    tx = contract_instance.functions.setFirstSymmetricKey(value).buildTransaction({'from': Account.from_key(key).address,'nonce': w3.eth.getTransactionCount(address), 'gas':3000000})
    signed_tx = w3.eth.account.signTransaction(tx, key)
    w3.eth.sendRawTransaction(signed_tx.rawTransaction)


def setValueTwo(w3, contract_instance, address, value, key):  
    tx = contract_instance.functions.setSecondSymmetricKey(value).buildTransaction({'from': Account.from_key(key).address,'nonce': w3.eth.getTransactionCount(address), 'gas':3000000})
    signed_tx = w3.eth.account.signTransaction(tx, key)
    w3.eth.sendRawTransaction(signed_tx.rawTransaction)

def getValueOne(contract_instance,key):
    return  contract_instance.functions.getFirstSymmetricKey().call({'from': Account.from_key(key).address, 'gas': 100000})

def getValueTwo(contract_instance,key):
    return  contract_instance.functions.getSecondSymmetricKey().call({'from': Account.from_key(key).address, 'gas': 100000})


load_dotenv()

keyProvider = os.getenv('PROVIDER_PRIV_KEY')
keyConsumer = os.getenv('CONSUMER_PRIV_KEY')
keyApplication = os.getenv('APPLICATION_PRIV_KEY')

cloudProvider = os.getenv('PROVIDER_PUB_ADDRESS')
cloudConsumer = os.getenv('CONSUMER_PUB_ADDRESS')
cloudApplication = os.getenv('APPLICATION_PUB_ADDRESS')


w3 = Web3(Web3.HTTPProvider(os.getenv('BLOCKCHAIN_SERVER')))

contract_instance = w3.eth.contract(address=contract.address, abi=contract.abi)

parameters = getSymmetricParameters(contract_instance,keyProvider)

g = parameters[0]
p = parameters[1]

#Set Value A
setValueOne(w3,contract_instance,cloudProvider,123,keyProvider)

#Set Value B
setValueOne(w3,contract_instance,cloudConsumer,456,keyConsumer)

#Set Value C
setValueOne(w3,contract_instance,cloudApplication,789,keyApplication)

#Get Value for CloudProvider
C = getValueOne(contract_instance,keyProvider)
#Get Value for CloudConsumer
A = getValueOne(contract_instance,keyConsumer)
#Get Value for CloudApplication
B = getValueOne(contract_instance,keyApplication)


a =  int(random.random() *100000)
b =  int(random.random() *100000)
c =  int(random.random() *100000)

A = (g ** a) % p
B = (g ** b) % p
C = (g ** c) % p



AB = A ** b % p
BC = B ** c % p
CA = C ** a % p

#Set Value AB
setValueTwo(w3,contract_instance,cloudConsumer,AB,keyConsumer)

#Set Value BC
setValueTwo(w3,contract_instance,cloudApplication,BC,keyApplication)

#Set Value CA
setValueTwo(w3,contract_instance,cloudProvider,CA,keyProvider)

#Get Value for CloudProvider
BC = getValueTwo(contract_instance,keyProvider)
#Get Value for CloudConsumer
CA = getValueTwo(contract_instance,keyConsumer)
#Get Value for CloudApplication
AB = getValueTwo(contract_instance,keyApplication)


print(BC ** a % p)
print(CA ** b % p)
print(AB ** c % p)

skey = AB ** c % p
skey = skey.to_bytes(16,'big')
header = b"header"
data = b"This is a super top secret"



cip = AES.new(skey, AES.MODE_GCM)
cip.update(header)

ciphertext, tag = cip.encrypt_and_digest(data)

print(ciphertext)
print(tag)


decipher = AES.new(skey, AES.MODE_GCM, nonce=cip.nonce)
decipher.update(header)
plaintext = decipher.decrypt_and_verify(ciphertext,tag)
print(plaintext)




latestBlock = w3.eth.get_block('latest')
while True:
    print('Polling Blockchain')
    currentBlock = w3.eth.get_block('latest')
    # Polling Code   
    time.sleep(10)
            
    

