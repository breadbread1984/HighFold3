#!/usr/bin/bash

# to prevent docker image include whole public database, build the image first
docker build -t alphafold3_cyclic -f docker/Dockerfile .
sudo bash fetch_databases.sh /srv/shared/public_databases
chmod 777 -R /srv/shared/public_databases
