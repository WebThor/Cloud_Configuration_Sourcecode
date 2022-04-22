from azure.mgmt.recoveryservicesbackup import RecoveryServicesBackupClient
from azure.mgmt.recoveryservicesbackup.models import IaasVMBackupRequest , OperationStatusValues
from azure.common.credentials  import ServicePrincipalCredentials
from datetime import datetime, timedelta, timezone
from msrest.paging import Paged
import re
import time
from dApp import contract
from six.moves.urllib.parse import urlparse
import os
from eth_typing.encoding import HexStr
from web3 import Web3
from web3.auto import w3
from eth_keys import keys
from eth_account.messages import encode_defunct
from dotenv import load_dotenv
import hashlib

#Load Environment Variables containing Azure and Blockchain credentials
load_dotenv()


"""
Here is the whole Blockchain communication managed
"""

#This function is used to store values at the Blockchain. It's the Blockchain <=> Cloud communication channel
def setBlockchainValue(w3, contract_instance, address, value, key):
    tx = contract_instance.functions.setStatus(value).buildTransaction({'from': Account.from_key(key).address,'nonce': w3.eth.getTransactionCount(address), 'maxFeePerGas': 2000000000, 'maxPriorityFeePerGas': 1000000000})
    signed_tx = w3.eth.account.signTransaction(tx, key)
    w3.eth.sendRawTransaction(signed_tx.rawTransaction)


#Retrieves the current stored and signed configuration from the Blockchain
def getConfigFromBlockchain(contract_instance,key):
    return  contract_instance.functions.getConfiguration().call({'from': Account.from_key(key).address, 'gas': 100000})

#Stores and signes the hash value of the current cloud instance at the Blockchain.
def storeHashToBlockchain(compute_client, w3, contract_instance, keyApplication):
    vm = compute_client.virtual_machines.get(GROUP_NAME, VM_NAME, expand='instanceView')
    #SHA512 is used as hash function to hash the taken application snapshot
    hashed_string = hashlib.sha512(vm).hexdigest()
    #Snapshot is stored on the Blockchain, using the applications' private key for sining the transaction
    setBlockchainValue(w3,contract_instance,os.getenv('APPLICATION_PUB_ADDRESS'), hashed_string , keyApplication)

def storeErrorToBlockchain(compute_client, w3, contract_instance, keyApplication):
    #An error occurred. Error code "0" is stored on the Blockchain
    setBlockchainValue(w3,contract_instance,os.getenv('APPLICATION_PUB_ADDRESS'), "0", keyApplication)


def triggerConfigurationSigning():

    #Create an authentication object
    credentials = ServicePrincipalCredentials(
    client_id= os.getenv('CLIENT_ID') ,
    secret= os.getenv('SECRET'),
    tenant= os.getenv('TENANT')
    )

    #Authenticate at the named Azure Subscription using the authentication object
    client=RecoveryServicesBackupClient(credentials=credentials,subscription_id= os.getenv('SUBSCRIPTION_ID'))
    filter_string="backupManagementType eq 'AzureIaasVM'"
    vm_name= os.getenv('VM_NAME')
    resource_group_name= os.getenv('RESOURCE_GROUP_NAME')
    vault_name= os.getenv('VAULT_NAME')

    retain_until = datetime.now(timezone.utc) + timedelta(days=30)

    res =client.backup_protected_items.list(
        vault_name=vault_name,
        resource_group_name=resource_group_name,
        filter=filter_string
    )
    items =list(res) if isinstance(res, Paged) else res

    item =[item for item in items if item.properties.friendly_name.lower() == vm_name.lower()]
    container_name=(re.search('(?<=protectionContainers/)[^/]+', item[0].id)).group(0)

    protected_item_name =(re.search('(?<=protectedItems/)[^/]+', item[0].id)).group(0)

    #Trigger a snapshot at Azure
    result =client.backups.trigger(
        vault_name=vault_name,
        resource_group_name=resource_group_name,
        fabric_name='Azure',
        container_name=container_name,
        protected_item_name=protected_item_name,
        parameters=IaasVMBackupRequest(recovery_point_expiry_time_in_utc=retain_until),raw=True
    )

    #Asynchronously check the operation status at Azure
    header =result.response.headers['Azure-AsyncOperation']
    parse_object = urlparse(header)
    id=parse_object.path.split("/")[-1]
    operation_status =client.backup_operation_statuses.get(
        vault_name=vault_name,
        resource_group_name=resource_group_name,
        operation_id=id
    )

    #Print hint while snapshot is not finished
    while operation_status.status == OperationStatusValues.in_progress:
        time.sleep(3)
        print("Snapshot ongoing")
        operation_status =client.backup_operation_statuses.get(
        vault_name=vault_name,
        resource_group_name=resource_group_name,
        operation_id=id
        )

    #Call function for creating hash value of successfull backup and store backup hash value at the Blockchain
    if operation_status.status == OperationStatusValues.completed:
        storeHashToBlockchain(client)

    #Store failure at the Blockchain
    if operation_status.status == OperationStatusValues.failed:
        storeErrorToBlockchain(client)

def applicationConfig(currentConfiguration):
    #Do Application Configuration here
    triggerConfigurationSigning()


#This is the main Blockchain polling funtion which continuesly runs once started and checks the Blockchain for configuration changes
def main():
    w3 = Web3(Web3.HTTPProvider(os.getenv('BLOCKCHAIN_SERVER')))
    contract_instance = w3.eth.contract(address=contract.address, abi=contract.abi)
    keyApplication = os.getenv('APPLICATION_PRIV_KEY')
    latestBlock = w3.eth.get_block('latest')
    latestConfig = getConfigFromBlockchain(contract_instance,keyApplication)
    while True:
        print('Polling Blockchain')
        currentBlock = w3.eth.get_block('latest')
        if currentBlock != latestBlock:
            latestBlock = currentBlock
            currentConfiguration = getConfigFromBlockchain(contract_instance,keyApplication)
            if latestConfig != currentConfiguration:
                latestConfig = currentConfiguration
                applicationConfig(currentConfiguration)
        time.sleep(10)
            


if __name__ == "__main__":
    main()