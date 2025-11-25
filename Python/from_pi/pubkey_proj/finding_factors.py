def is_prime(num):

    divis_list = []

    # Add divisible numbers to list
    for i in range(2, num - 1):
        if num % i == 0:
            divis_list.append(i)

    # If nothing is added to the list,
    # the number is prime
    if len(divis_list) != 0:
        print("Not prime.")
    else:
        print("Prime!")

    # If the list has numbers,
    # print out the factors
    if len(divis_list) > 0:
        for i in divis_list:
            print("%s is a factor of %s." % (i, num))


number = int(input("Enter a number: "))

is_prime(number)



