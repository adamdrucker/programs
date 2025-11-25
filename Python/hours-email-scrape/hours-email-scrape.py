#!/usr/bin/python3

'''
TODO

* open new file and write output to it
* remove duplicate lines
* find a way to organize all lines
    * 1) nothing special at start
    * 2) starts with "ONSITE"
    * 3) starts with "TKD"
'''

from datetime import datetime
import sys

# current date
current_datetime = datetime.now().strftime("%Y-%m-%d")
str_current_datetime = str(current_datetime)

# actually the headers for each client
footers = ("ENGAGING", "HOLYOKE", "NEURO", "ORCD", "SATORI", "Total")

# search pattern for item lines
pattern = " *"

#def main():

# def scrape_email():

# file for scraping out raw garbage data
scraped_file = open("scraped_email_"f"{str_current_datetime}"".txt", "w")
# file for adding tabbed lines of refined data
tabbed_file = open("tabbed_email_"f"{str_current_datetime}"".txt", "w")

# first arg is raw email file passed in
hours_email = sys.argv[1] if len(sys.argv[1]) > 1 else None
if hours_email:
    # open file and read its contents by line
    with open(hours_email, "r") as open_email_file:
        lines = open_email_file.readlines()
        # for each line fine specific ones and write them to the scraped file
        for i in lines:
            if i.startswith("####") or i.startswith(" *") or i.startswith(footers):
                scraped_file.write(i)

scraped_file = "scraped_email_"f"{str_current_datetime}"".txt"
with open(scraped_file, "r") as open_scraped_file:
    lines = open_scraped_file.readlines()
    for i in lines:
        if pattern in lines:
            tabbed_file.write(i)

# with open(new_file, "r") as opened_new_file:
#     for line in opened_new_file:
#         if line.starts(" *"):
#             print(line)
