# The mode is the value the occurs the most in a data set
# There can be more than one modal value

from collections import Counter

iVal = input("Enter a number for mode calculation (q to quit): ")
iList = []  # Init empty list

# Append input to list
while iVal != 'q':
    iList.append(int(iVal))
    iVal = input("Enter a number for mode calculation (q to quit): ")

iCount = Counter(iList)


def mode():

    iModeList = []  # Init blank list
    iMaxList = []   # Init blank list

    # Append all dict values to list
    for i in iCount.values():
        iModeList.append(i)

    # Init max value variable
    iMax = max(iModeList)

    # Find keys paired with max value
    for key, val in iCount.items():
        if iMax == val:
            iMaxList.append(key)
    return iMaxList


mode()


if len(mode()) == 1:
    print("Mode:", ', '.join((map(str, mode()))), "--> Unimodal!")
elif len(mode()) == 2:
    print("Mode:", ', '.join((map(str, mode()))), "--> Bimodal!")
elif len(mode()) > 2:
    print("Mode:", ', '.join((map(str, mode()))), "--> Multimodal!")

# Will have to change the output statement to print the values in ascending order
