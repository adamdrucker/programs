#!/bin/bash

echo "PAYCODES"
echo "========"
echo "1) MGHPCC/INTERN"
echo "2) ENGAGING"
echo "3) SATORI"
echo "4) NEUHPC"
echo "5) LUNCH"
echo "6) Other"
echo -n "Select a paycode: "
read code;

case $code in
	"1") PAYCODE="MGHPCC/INTERN"	;;
	"2") PAYCODE="ENGAGING"				;;
	"3") PAYCODE="SATORI"					;;
	"4") PAYCODE="NEUHPC"					;;
	"5") PAYCODE="LUNCH"					;;
	"6") echo -n  Type in paycode: ; read PAYCODE
esac

echo $PAYCODE
