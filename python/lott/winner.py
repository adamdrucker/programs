# 1. take repeated input of a list of 5 digits
# 2. append the value of each index (0-4) to its own list
# 3. calculate the modal value for each index list in the form of a list

from collections import Counter


first = []
second = []
third = []
fourth = []
fifth = []

n = input("Continue?: ")
while n != "n":

    input_string = input("Enter 5 digits separated by spaces: ")

    num_list = input_string.split()

    first.append(num_list[0])
    second.append(num_list[1])
    third.append(num_list[2])
    fourth.append(num_list[3])
    fifth.append(num_list[4])

    n = input("Continue?: ")
    continue

oneCount = Counter(first)
twoCount = Counter(second)
threeCount = Counter(third)
fourCount = Counter(fourth)
fiveCount = Counter(fifth)


def mode(h):

    iModeList = []  # Init blank list
    iMaxList = []   # Init blank list

    # Append all dict values to list
    for i in h.values():
        iModeList.append(i)

    # Init max value variable
    iMax = max(iModeList)

    # Find keys paired with max value
    for key, val in h.items():
        if iMax == val:
            iMaxList.append(key)
    return iMaxList


one = mode(oneCount)
two = mode(twoCount)
three = mode(threeCount)
four = mode(fourCount)
five = mode(fiveCount)

results = [one, two, three, four, five]
print(results)

# if len(mode()) == 1:
#     print("Mode:", ', '.join((map(str, mode()))), "--> Unimodal!")
# elif len(mode()) == 2:
#     print("Mode:", ', '.join((map(str, mode()))), "--> Bimodal!")
# elif len(mode()) > 2:
#     print("Mode:", ', '.join((map(str, mode()))), "--> Multimodal!")