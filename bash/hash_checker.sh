#!/bin/bash

echo -n "Enter the hash provided by the vendor: "
read VHASH

echo " "
echo -n "Enter the hash from your calculation: "
read MHASH

if [ $VHASH == $MHASH ]
then
	echo ""
	echo "Hashes match."
else
	echo ""
	echo "Hashes don't match."
fi
