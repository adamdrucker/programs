#!/usr/bin/env/python

# This script requires Python 3.9 due to some built-in functions used.
# This script also requires pandas.

import os
import glob
import pandas as pd


userName = os.environ['USER']
hoursdir = f"/home/hours/{userName}/hoursapp/hours/*"

# local test variables
un = "adrucker"
hours_dir = "/home/adam/Documents/Python/counter/hours/*"
p_hours_dir = "/home/adam/Documents/Python/counter/hours/"

billingDict = {}
hours_list = []

'''
TODO: 
    1) glob needs to only read non-dot and non-release files, nor directories
        * it doesn't seem like this script reads hidden files!
    2) the script needs logic to start counting on mondays each week and know where
        mondays are relative to the current day in order to go backwards
    3) to start, the successful output should be emailed to the user
    4) if someone - on a thursday - goes back and edits their file from monday,
        altering the last mod date (?) will it break the script?
    5) consider changing the glob method for finding most recently modified files
        to just sorting the directory contents (therefore things won't be read 
        out of order if #4 occurs)
'''


counter = int(-1)

# newest file
latest_file = sorted(glob.iglob(f'{hours_dir}'))[counter]
# base name of newest fle
lf = os.path.basename(latest_file)

# strip username from filename
file_date = lf.removesuffix(f'-{un}') # this method is Python 3.9

# get day of week from stripped date
dow = pd.Timestamp(f'{file_date}').day_name() # this is pandas


while dow != "Monday":
    hours_list.append(f"{p_hours_dir}{lf}")
    counter -= 1
    lf = os.path.basename(sorted(glob.iglob(f'{hours_dir}'))[counter])
    file_date = lf.removesuffix(f'-{un}') # this method is Python 3.9
    dow = pd.Timestamp(f'{file_date}').day_name() # this is pandas

if dow == "Monday":
    hours_list.append(f"{p_hours_dir}{lf}")

'''
    THERE NEEDS TO BE A CONDITION THAT TELLS THE SCRIPT TO STOP
    GOING THRU FILES ONCE IT HITS A MONDAY, REGARDLESS OF HOW MANY
    OTHER FILES ARE IN THE DIR
    
    2) this might already work =)
'''

# # iterate through all files in dir
# for file in glob.iglob(f"{hours_dir}"):
for file in hours_list:

    f = open(f"{file}", "r")

    for i in f:

        # for every line in the file delimit by the pipe
        delim = i.split('|')

        # take the index position of the billing code
        billing_code = delim[4]

        # take the index position of the hours logged
        hour_count = delim[3]

        # add code to dict keys
        if billing_code not in billingDict.keys():
            billingDict[billing_code] = 0

        # add hour count to dict values
        if billing_code in billingDict.keys():
            billingDict[billing_code] += float(hour_count)

    f.close()

print("Your current weekly hours are as follows: ")
for i, (j,k) in enumerate(billingDict.items()):
    print(f'{j}: {k}')

