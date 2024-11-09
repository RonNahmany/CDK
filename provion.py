from enum import Enum


class install_docker(Enum):
    script ="#!/bin/bash;sudo yum update -y;sudo yum install -y ca-certificates curl;sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/7/docker-ce.repo;sudo yum update -y;sudo yum install -y docker-ce docker-ce-cli containerd.io;sudo groupadd docker;sudo usermod -aG docker $USER"

#print(install_docker.script.value)
