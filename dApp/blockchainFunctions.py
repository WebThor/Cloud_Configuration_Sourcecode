
from eth_account import Account


def getSymmetricParameters(contract_instance,key):
    return  contract_instance.functions.getSymmetricParameters().call({'from': Account.from_key(key).address, 'gas': 100000})

def getConfiguration(contract_instance,key):
    return  contract_instance.functions.getConfiguration().call({'from': Account.from_key(key).address, 'gas': 100000})

def setConfiguration(w3, contract_instance, address, _c,_t, key):
    tx = contract_instance.functions.setConfiguration(_c,_t).buildTransaction({'from': Account.from_key(key).address,'nonce': w3.eth.getTransactionCount(address), 'maxFeePerGas': 2000000000, 'maxPriorityFeePerGas': 1000000000})
    signed_tx = w3.eth.account.signTransaction(tx, key)
    w3.eth.sendRawTransaction(signed_tx.rawTransaction)


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