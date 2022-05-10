import os
from eth_typing.encoding import HexStr
from web3 import Web3
from web3.auto import w3
from eth_keys import keys
from eth_account.messages import encode_defunct
import random
import contract
import hashlib
import consumerManagementScript
import blockchainFunctions
import time
from dotenv import load_dotenv




load_dotenv()


keyConsumer = os.getenv('CONSUMER_PRIV_KEY')
cloudConsumer = os.getenv('CONSUMER_PUB_ADDRESS')


w3 = Web3(Web3.HTTPProvider(os.getenv('BLOCKCHAIN_SERVER')))

contract_instance = w3.eth.contract(address=contract.address, abi=contract.abi)

parameters = blockchainFunctions.getSymmetricParameters(contract_instance,keyConsumer)
configuration = blockchainFunctions.getConfiguration(contract_instance,keyConsumer)

skey = consumerManagementScript.keyManagementFlow(w3,contract_instance,cloudConsumer,keyConsumer,parameters[0],parameters[1])


latestBlock = w3.eth.get_block('latest')
latestParameters = hashlib.sha1(parameters).hexdigest()
latestConfiguration = hashlib.sha1(configuration).hexdigest()



while True:
    print('Polling Blockchain')
    currentBlock = w3.eth.get_block('latest')
    if latestBlock != currentBlock:
        latestBlock = currentBlock
        parameters = blockchainFunctions.getSymmetricParameters(contract_instance,keyConsumer)
        currentParameters = hashlib.sha1(parameters).hexdigest()
        #First Communication Flow
        if latestParameters != currentParameters:
            latestParameters = currentParameters
            skey= consumerManagementScript.keyManagementFlow(w3, contract_instance,cloudConsumer,keyConsumer,parameters[0],parameters[1])
        
        #Second Communication Flow
        if latestConfiguration


    time.sleep(1000)
            
    

