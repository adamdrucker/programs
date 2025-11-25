# ///////////////////////////////////
# Mersenne prime number finder
# written by adam drucker (2021-2022)
# ///////////////////////////////////

'''
    A Mersenne prime is a number that is one less than a power of two.
    For example: 2^2-1 (two to the power of two, minus one)
'''

import sys

def main(): 
    
    # script takes in a number
    num = int(sys.argv[1])

    def mersenne_num(num):
        return 2 ** num -1
    
    




if __name__ == 'main':
    main()