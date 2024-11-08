from collections import defaultdict
from enum import Enum
import boto3

region = defaultdict()
region["israel"] = "il-central-1"
region["us"] = "us-east-1"

def get_azs(region):
    clinet = boto3.client('ec2', region_name = region)
    reponce = clinet.describe_availability_zones()
    avilable_zones = [zone['ZoneName'] for zone in reponce['AvailabilityZones']]
    print(avilable_zones)








get_azs("il-central-1")

