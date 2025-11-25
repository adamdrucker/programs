# //////////////////////////////////////
#  Convert a binary byte to decimal
# ///////////////////////////////////

def binconv():

    sChoice = 'y'
    while sChoice == 'y':
        sChoice = input("Perform binary conversion? (y/N): ").lower()
        nBin_Input = input("Enter a binary byte: ")

        # Rejects input greater or less than 8 bits in length
        if len(nBin_Input) < 8 or len(nBin_Input) > 8:
            print("Your entry has too many or too few bits.")
            print("Please make sure your byte is eight bits long.")

        for i in nBin_Input:
            if int(i) < 0 or int(i) > 1:
                print("Please enter only 0's or 1's.")
                break
            else:
                if len(nBin_Input) == 8:
                    bin_list = [i for i in nBin_Input]  # Creates a list from the input

                    nOnePos = int(bin_list[7])*1      # Multiplies input by the 1 position
                    nTwoPos = int(bin_list[6])*2      # Multiplies input by the 2 position
                    nFourPos = int(bin_list[5])*4     # Multiplies input by the 4 position
                    nEightPos = int(bin_list[4])*8    # Multiplies input by the 8 position
                    nSxtnPos = int(bin_list[3])*16    # Multiplies input by the 16 position
                    nThrTwoPos = int(bin_list[2])*32  # Multiplies input by the 32 position
                    nSxtFoPos = int(bin_list[1])*64   # Multiplies input by the 64 position
                    nOtePos = int(bin_list[0])*128    # Multiplies input by the 128 position

                    nBin_Sum = int(nOnePos + nTwoPos + nFourPos + nEightPos + nSxtnPos + nThrTwoPos + nSxtFoPos + nOtePos)

                    if nBin_Sum >= 256:  # Checks to make sure the byte is not above 255
                        print("Please enter only 0's or 1's.")
                    else:
                        print(f"Your decimal number is {nBin_Sum}.")
                        sChoice = input("Perform another binary conversion? (y/N): ").lower()
                        if sChoice == 'y':
                            nBin_Input = input("Enter a binary byte: ")
                        else:
                            break
        if sChoice == 'n':
            print("Goodbye!")
            break


