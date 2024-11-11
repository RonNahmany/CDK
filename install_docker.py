from enum import Enum


class InstallDocker(Enum):
    script = """#!/bin/bash
    sudo yum update -y
    sudo yum install -y yum-utils device-mapper-persistent-data lvm2
    sudo amazon-linux-extras install docker
    sudo yum install docker -y
    sudo systemctl start docker
    sudo systemctl enable docker
    """
