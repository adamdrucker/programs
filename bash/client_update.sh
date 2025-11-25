#!/bin/bash

# 2022 May 13 -- changed 'git pull origin master' to just 'git pull'

today=$(date '+%m-%d-%Y')

touch /home/adam/Techsquare/tmp/$today

for i in $(ls -ld /home/adam/Techsquare/clients/*/docs | awk '{print $9}')
	do
		cd $i
		GIT_SSH_COMMAND='ssh -i /home/adam/.ssh/client-pull -o IdentitiesOnly=yes' git pull
		if [ $? == 0 ]; then
			echo -e $i	"\t-->\t SUCCESS" >> /home/adam/Techsquare/tmp/$today
		else
			echo -e $i	"\t-->\t FAILURE" >> /home/adam/Techsquare/tmp/$today
		fi
	done	
		
mail -s 'Client pull status' adrucker@techsquare.com <<< $(cat /home/adam/Techsquare/tmp/$today)
rm /home/adam/Techsquare/tmp/$today
