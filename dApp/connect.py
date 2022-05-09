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
    tx = contract_instance.functions.setFirstSymmetricKey(value).buildTransaction({'from': Account.from_key(key).address,'nonce': w3.eth.getTransactionCount(address), 'maxFeePerGas': 2000000000, 'maxPriorityFeePerGas': 1000000000})
    signed_tx = w3.eth.account.signTransaction(tx, key)
    w3.eth.sendRawTransaction(signed_tx.rawTransaction)


def setValueTwo(w3, contract_instance, address, value, key):  
    tx = contract_instance.functions.setSecondSymmetricKey(value).buildTransaction({'from': Account.from_key(key).address,'nonce': w3.eth.getTransactionCount(address), 'maxFeePerGas': 2000000000, 'maxPriorityFeePerGas': 1000000000})
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


latestBlock = w3.eth.get_block('latest')
while True:
    print('Polling Blockchain')
    currentBlock = w3.eth.get_block('latest')
    # Polling Code   
    time.sleep(10)
            
    

