#!/bin/bash
apt-get update
apt-get upgrade
apt-get install docker.io -y
apt-get install curl -y
curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
systemctl start docker
systemctl enable docker

