from abc import ABC
from logging import basicConfig
from eth_typing.encoding import HexStr
from web3 import Web3
from web3.auto import w3
from eth_keys import keys
from eth_account.messages import encode_defunct
import random


def signMessage(message, privateKey):
    message = encode_defunct(text=message)
    signed_message = w3.eth.account.sign_message(message, private_key=privateKey)
    return signed_message

def verifyMessage(message, signed_message):
    message = encode_defunct(text=message)
    return w3.eth.account.recover_message(message, signature=signed_message.signature)

p = 66879465661348111229871989287968040993513351195484998191057052014006844134449
g = 46316835



a =  int(random.random() *100000)
b =  int(random.random() *100000)
c =  int(random.random() *100000)

A = (g ** a) % p
B = (g ** b) % p
C = (g ** c) % p

AB = A ** b % p
BC = B ** c % p
CA = C ** a % p



print(A)
print(B)
print(C)

print(AB ** c % p)
print(BC ** a % p)
print(CA ** b % p)


keyProvider = '0x09022e589dfd7c7bd451d4ff52b1b118f7e74f6fcd06cf091c00f847d82ba1f3'
keyConsumer = '0x3f58a4fef9bf270172d70444b981af926a2e6802dfad2db4a78c526a9de709c5'
keyApplication = '0x692877747efbf365bab42c1fa765df4eddce83219f58f87f9314846f28021004'
keyProviderByteString = Web3.toBytes(hexstr=keyProvider)

keyConsumerByteString = Web3.toBytes(hexstr=keyConsumer)
keyApplicationByteString = Web3.toBytes(hexstr=keyApplication)

pkProvider = keys.PrivateKey(keyProviderByteString)
pkConsumer = keys.PrivateKey(keyConsumerByteString)
pkApplication = keys.PrivateKey(keyApplicationByteString)


#print(pkProvider.public_key)
#print(pkProvider.public_key.to_checksum_address())
#print(pkConsumer.public_key)
#print(pkApplication.public_key)


signed_message = signMessage(str(pkProvider.public_key),keyProviderByteString)
#print(signed_message)

#print(verifyMessage(str(pkProvider.public_key), signed_message))

w3 = Web3(Web3.HTTPProvider('http://51.116.116.230:8545'))



#print(w3.isConnected())
#print(w3.eth.get_block(3))
#print(w3.eth.get_block('latest'))

