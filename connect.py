from abc import ABC
from logging import basicConfig
from eth_typing.encoding import HexStr
from web3 import Web3
from web3.auto import w3
from eth_keys import keys
from eth_account.messages import encode_defunct
import random
import contract
from eth_account import Account


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

keyProvider = '0x09022e589dfd7c7bd451d4ff52b1b118f7e74f6fcd06cf091c00f847d82ba1f3'
keyConsumer = '0x3f58a4fef9bf270172d70444b981af926a2e6802dfad2db4a78c526a9de709c5'
keyApplication = '0x692877747efbf365bab42c1fa765df4eddce83219f58f87f9314846f28021004'

cloudProvider = '0xD429D86D0e4eC82bC8f26b0bda68F89F4Cb4b468'
cloudConsumer = '0xA863d6B63f8524fbbD16A080F7e0C0865d19bd73'
cloudApplication = '0xd2DFF497cAaBA3fd4e70D144616f5Bf27fA6f8f2'


w3 = Web3(Web3.HTTPProvider('http://51.116.116.230:8545'))

contract_instance = w3.eth.contract(address=contract.address, abi=contract.abi)

#Set Value A
setValueOne(w3,contract_instance,cloudProvider,123,keyProvider)

#Set Value B
setValueOne(w3,contract_instance,cloudConsumer,456,keyConsumer)

#Set Value C
setValueOne(w3,contract_instance,cloudApplication,789,keyApplication)

#Get Value for CloudProvider
print(getValueOne(contract_instance,keyProvider))
#Get Value for CloudConsumer
print(getValueOne(contract_instance,keyConsumer))
#Get Value for CloudApplication
print(getValueOne(contract_instance,keyApplication))

#Set Value A
setValueTwo(w3,contract_instance,cloudProvider,1111,keyProvider)

#Set Value B
setValueTwo(w3,contract_instance,cloudConsumer,2222,keyConsumer)

#Set Value C
setValueTwo(w3,contract_instance,cloudApplication,3333,keyApplication)

#Get Value for CloudProvider
print(getValueTwo(contract_instance,keyProvider))
#Get Value for CloudConsumer
print(getValueTwo(contract_instance,keyConsumer))
#Get Value for CloudApplication
print(getValueTwo(contract_instance,keyApplication))





#a =  int(random.random() *100000)
#b =  int(random.random() *100000)
#c =  int(random.random() *100000)

#A = (g ** a) % p
#B = (g ** b) % p
#C = (g ** c) % p

#AB = A ** b % p
#BC = B ** c % p
#CA = C ** a % p



#print(A)
#print(B)
#print(C)

#print(AB ** c % p)
#print(BC ** a % p)
#print(CA ** b % p)




#print(w3.isConnected())
#print(w3.eth.get_block(3))
#print(w3.eth.get_block('latest'))

