#!/bin/bash

spin()
{
	# backwards
  #spinner="/|\\-/|\\-"
	# forwards
	spinner="\\|/-\\|/-"
  while :
  do
    for i in `seq 0 7`
    do
      echo -n "${spinner:$i:1}"
      echo -en "\010"
      sleep .1
    done
  done
}

spin
