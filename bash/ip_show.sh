#!/bin/bash

A=$(ip -br -c addr show | awk '{print $1, $2, $3}')
B=$(ip -br -c link show | awk '{print $3}')

echo $A $B

