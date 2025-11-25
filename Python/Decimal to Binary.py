# /////////////////////////////////
#  Convert decimal to binary byte
# //////////////////////////////

nDec_Input = int(input("Enter a whole integer less than 256: "))
if nDec_Input >= 256:
    print("Your entry must be 255 or less.")

newBin_List = []  # Creating a list for the bits
newBin_Counter = 0

if nDec_Input >= 128:
    newBin_List.insert(0, 1)
    newBin_Counter = nDec_Input - 128
elif nDec_Input < 128:
    newBin_List.insert(0, 0)


if nDec_Input < 128 and nDec_Input >= 64:
    newBin_List.insert(1, 1)
    newBin_Counter = newBin_Counter - 64
else:
    newBin_List.insert(1, 0)


if nDec_Input < 64 and nDec_Input >= 32:
    newBin_List.insert(2, 1)
    newBin_Counter = newBin_Counter - 32
else:
    newBin_List.insert(2, 0)


if nDec_Input < 32 and nDec_Input >= 16:
    newBin_List.insert(3, 1)
    newBin_Counter = newBin_Counter - 16
else:
    newBin_List.insert(3, 0)


if nDec_Input < 16 and nDec_Input >= 8:
    newBin_List.insert(4, 1)
    newBin_Counter = newBin_Counter - 8
else:
    newBin_List.insert(4, 0)


if nDec_Input < 8 and nDec_Input >= 4:
    newBin_List.insert(5, 1)
    newBin_Counter = newBin_Counter - 4
else:
    newBin_List.insert(5, 0)


if nDec_Input < 4 and nDec_Input >= 2:
    newBin_List.insert(6, 1)
    newBin_Counter = newBin_Counter - 2
else:
    newBin_List.insert(6, 0)


if nDec_Input < 2 and nDec_Input >= 1:
    newBin_List.insert(7, 1)
    newBin_Counter = newBin_Counter - 1
else:
    newBin_List.insert(7, 0)


for i in newBin_List:
    print(i, end="")

'''
if nVar1 >= 32:
    newBin_List.insert(2, 1)
else:
    newBin_List.insert(2, 0)

if nVar1 >= 16:
    newBin_List.insert(3, 1)
else:
    newBin_List.insert(3, 0)

if nVar1 >= 8:
    newBin_List.insert(4, 1)
else:
    newBin_List.insert(4, 0)

if nVar1 >= 4:
    newBin_List.insert(5, 1)
else:
    newBin_List.insert(5, 0)

if nVar1 >= 2:
    newBin_List.insert(6, 1)
else:
    newBin_List.insert(6, 0)

if nVar1 % 2 != 0:
    newBin_List.insert(7, 1)
else:
    newBin_List.insert(7, 0)

for i in newBin_List:
    print(i, end="") '''