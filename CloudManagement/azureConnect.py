from azure.mgmt.compute.models import DiskCreateOption
from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
import os

credential = AzureCliCredential()
subscription_id = '384409a3-56ad-410f-a0e7-04554439dcb0'


# Constants we need in multiple places: the resource group name and the region
# in which we provision resources. You can change these values however you want.
RESOURCE_GROUP_NAME = "PhD"
LOCATION = "Germany West Central"

compute_client = ComputeManagementClient(credential, subscription_id)
