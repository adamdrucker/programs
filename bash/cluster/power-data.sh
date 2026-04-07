#!/bin/bash

if [[ "$1" == "-h" || $# -eq 0 ]]; then
      echo "usage: power-data.sh <nodeset> <flags> <-o> <output-file>"
      echo "-h  show help for ipmitool dcmi power reading"
      echo "-ins  instantaneous power reading"
      echo "-min  minimum during sampling period"
      echo "-max  maximum during sampling period"
      echo "-avg  average during sampling period"
      echo "-sen  pull power consumption from sensor data"
      echo "-o  specify output file"
      exit 0
fi

nodeset=$1
shift

while test $# -gt 0; do
  case "$1" in
    -ins) grep_term="Instantaneous power reading:"	;;
    -min) grep_term="Minimum during sampling period:"	;;
    -max) grep_term="Maximum during sampling period:"	;;
    -avg) grep_term="Average power reading"		;;
    -sen) do_sensor=true				;;
    -o) output_file="$2"; shift				;;
    *) echo "unknown flag, use -h for help"; exit 1	;;
  esac
  shift
done

output="tee /dev/stdout"
if [[ -n "${output_file}" ]]; then
  output="tee ${output_file}"
else
  output="cat"
fi

# dcmi power reading via ipmitool
if [[ -n "${grep_term}" ]]; then 
  clush -b -w ${nodeset} "ipmitool dcmi power reading | grep '${grep_term}'" | ${output}
fi

# sensor reading via ipmitool
if [[ ${do_sensor} == true ]]; then
  clush -b -w ${nodeset} "ipmitool sensor | grep 'Pwr Consumption'" | ${output}
fi


