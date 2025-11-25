import sys

num = int(sys.argv[1])
#num = int(input("Search through range up to: "))
p_list = []         # number list to check for primes
m_list = []         # mersenne list after prime check

# Mersenne prime is two to the power of n minus one
# if numbers in this list exponentiated by 2, minus 1, are prime, they are mersenne
for n in range(2, num + 1):

    # perform calculation to get number to be tested
    m_num = 2 ** n - 1

    # append that number to a list of potential primes
    # if a number in this list is prime then it is mersenne
    p_list.append(m_num)


for i in p_list:
    if i > 1:
        for x in range(2, i):
            if i % x == 0:
                break
        else:
            m_list.append(i)


print(m_list)



