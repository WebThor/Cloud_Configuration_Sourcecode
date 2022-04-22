# Welcome

This Git repository contains the complete source code used to evaluate the architecture named in the paper **Blockchain-Based Reference Architecture for Automated, Transparent, and Notarized Attestation of Compliance Adaptations** (link to paper follows, as soon as it gets published). The code is subject to the MIT license.

# Background

Enterprises have to meet the compliance requirements defined by the International Standards Organization (ISO) 27000-series, British Standard (BS) 7799, Payment Card Industry Data Security Standard (PCI-DSS), Information Technology Infrastructure Library (ITIL), or Control Objectives for Information and related Technology (COBIT) [6]. However, enterprises have only limited control over whether the requirements stipulated in their standards are implemented using cloud services. Enterprises must trust cloud providers to ensure that agreements are fulfilled as negotiated and that the provided data will not fall into the wrong hands. This trust includes, for example, the specified data storage location. The enterprise must trust that all its data will be stored as contractually agreed. Transparency is an important mechanism responsible for removing the trust barrier between enterprises and cloud application providers. The attached code allow for a transparent, tracable, and automated adjustments of cloud configurations. 

# Files
The repository is divided into three folders and two files.

In the Order Blockchain, there is the **Management Smart Contract**. This was written in Solidity and is the central core of the process. The contract was written in Solidity and must be deployed on the Ethereum Blockchain.

The CloudManagement folder contains the **Cloud Management Script**, which must be executed on the cloud instance. The cloud management script only needs to be completed when the cloud application is started.

The dApp folder contains the source code for the **Client Management Script**. This can be adapted to the customer as desired.

## .env_sample

The file contains the environment variables needed to operate the architecture. Within the .env file, all necessary credentials are stored.

## requirements.txt

This file lists all required python packages to run the provided scripts.

# Setup
This section briefly describes how to use the developed code. The use of the Ethereum Blockchain is crucial here, as it forms the core of the work. Please also note that this is code for MS Azure. **A replacement of the code with other cloud vendors, or even running it locally is possible**

## .env
You must first provide all the necessary credentials in the .env file to get started. Please note that the code provided here is a demo. In a production environment, only a blockchain address and private address need to be specified in the .env. The dApp stored here simulates the communication of all Application Provider, Application Consumer, and Application.

	BLOCKCHAIN_SERVER = <"IP:PORT" of the Blockchain RPC>

	CLIENT_ID = <Azure Client ID>
	SECRET = <Azure Credentials>
	TENANT= <Azure Tenant ID>
	SUBSCRIPTION_ID = <Azure Subscription ID>

	VM_NAME = <Name of the VM,which should be backuped>
	RESOURCE_GROUP_NAME = <Resource name where to store the backup>
	VAULT_NAME = <The Vault name in which the backup should be stored>

	PROVIDER_PRIV_KEY = <Private Ethereum Key of the Application Provider>
	CONSUMER_PRIV_KEY = <Private Ethereum Key of the Application Consumer>
	APPLICATION_PRIV_KEY = <Private Ethereum Key of the Cloud Application>

	PROVIDER_PUB_ADDRESS = <Public Ethereum Addesss of the Cloud Application>
	CONSUMER_PUB_ADDRESS = <Public Ethereum Addesss of the Cloud Application>
	APPLICATION_PUB_ADDRESS = <Public Ethereum Addesss of the Cloud Application>


## Blockchain Smart Contract Deployment

The core of this work is the **Management Smart Contract**, which is contained in the "Blockchain" folder. This must first be deployed on an Ethereum blockchain. The deployment can be done using [Remix](https://remix.ethereum.org/). 

>Alternatively, an existing contract already deployed at on IP http://20.113.30.8:8545 and address 0x45bC89D15dd2730D072C681A7A3DDC037528D3cf can be used.

Depending on the use case, a cloud application provider may need to deploy multiple smart contracts for a customer. To keep track of the published smart contracts, an **Address Book Smart Contract** is also supplied in addition to the management smart contract. The address book smart contract can use this to store the addresses of several smart contracts in a single smart contract.

## Cloud Management Script

The **Cloud Management Script** must initially be started only on the Cloud application. It automatically checks whether a new application configuration is available. In function *applicationConfig*, you just have to specify which cloud application is to be configured.

	def applicationConfig(currentConfiguration):
		#Do Application Configuration here
		triggerConfigurationSigning()
## dApp 
In the folder dApp, there is currently a test **Customer Management Script** , which simulates the Application Customer and the Application Client, and the Application itself. The current script first negotiates a common symmetric key via a three-party Diffie Hellmann protocol. The dApp then encrypts a message using the negotiated symmetric key. Finally, it stores the encrypted message signed with the application customer's key in the cloud, retrieves it with the Application's key, and decrypts the message.

An end-user must split the dApp script among the three participants in a productive environment. However, the dApp script is sufficient for demonstrating the capability and testing the cloud application, as it calls all the necessary blockchain functions. 


# Synchronization

Details about the interaction of the application can be found in the paper  **Blockchain-Based Reference Architecture for Automated, Transparent, and Notarized Attestation of Compliance Adaptations**