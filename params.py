from collections import defaultdict
from enum import Enum
from os import access
import boto3
from Credencials import Cred

azs = []
CN_TO_region = defaultdict()
CN_TO_region["israel"] = "il-central-1"
CN_TO_region["us"] = "us-east-1"




def get_azs():
    region = CN_TO_region[Cred.country_Region.value.casefold()]
    clinet = boto3.client('ec2', region_name = region  ,aws_access_key_id=Cred.Access.value, aws_secret_access_key=Cred.Secret.value)
    reponce = clinet.describe_availability_zones()
    avilable_zones = [zone['ZoneName'] for zone in reponce['AvailabilityZones']]
    for item in avilable_zones:
        azs.append(item)
    return azs[0]

def get_region_from_CN():
    if Cred.country_Region.value.casefold() in CN_TO_region:
        return CN_TO_region[Cred.country_Region.value.casefold()]



# result =get_azs()
# print(result)

