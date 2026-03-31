#!/bin/bash

# launch sshuttle
sshuttle -r root@satori-route.mit.edu 192.168.0.0/16 172.30.0.0/16 172.16.0.0/16 172.29.0.0/16

# run python script
python3 /home/adam/Documents/Python/satori-checks.py
