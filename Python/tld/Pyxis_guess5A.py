# //////////////////////////////////////////
# *~* Abyssea Treasure Casket Game *~*
# ///////////////////////////////////////

# Modules
# //////////////////////////////////////
from random import randint
import time

# Init main variables
# //////////////////////////////////////
result = str(randint(10, 99))               # Random answer generated at start of sequence
result_sum = int(result[0]) + int(result[1])
first_dig = result[0]
second_dig = result[1]

# Opening dialogue
# //////////////////////////////////////
print("While travelling across a field you stumble upon a small, sturdy pyxis amidst a patch of tall grass.")
time.sleep(1)
print("It appears to be locked tight by some force beyond your reckoning.")
time.sleep(1)
print("A soft whisper echoes in your mind.")
time.sleep(1)
print('"You have five attempts to open the chest by guessing the correct combination..."')
time.sleep(1)


'''         There are 5 attempts to deduce the combination 
            to a locked chest, with each subsequent 
            incorrect guess prompting
            a hint to be displayed.
'''

# Init main program
# //////////////////////////////////////


def main():

    attempts = 0

    while attempts < 5:

        # == First hint ==
        def hint_sum():
            # result_sum = int(result[0]) + int(result[1])
            print(f"You sense the sum of the two digits is {result_sum}.")


        # == Second hint ==
        def hint_int():
            # /// Init variables ///
            digit_type_hint = randint(0, 1)
            # first_dig = result[0]
            # second_dig = result[1]

            # // Logic ///
            if first_dig == second_dig:
                pr_str = "*~## PHANTOM ROLL! ##~*\n"    # Buffs from COR applied for this turn
                # Should this be made into its own func then called with string as arg?
                for char in pr_str:
                    print(char, end='')
                    time.sleep(0.25)
                print("Buffs applied!")
                time.sleep(1)
                print("You sense the two digits are the same number.")

                time.sleep(1)
            elif digit_type_hint == 0 and int(first_dig) % 2 == 0:
                print("You sense the first digit is even.")

                time.sleep(1)
            elif digit_type_hint == 0 and int(first_dig) % 2 != 0:
                print("You sense the first digit is odd.")

                time.sleep(1)
            elif digit_type_hint == 1 and int(second_dig) % 2 == 0:
                print("You sense the second digit is even.")

                time.sleep(1)
            elif digit_type_hint == 1 and int(second_dig) != 0:
                print("You sense the second digit is odd.")

                time.sleep(1)

        # == Third hint ==
        def hint_range():
            # /// Init variables ///
            g_than = int(result) - randint(10, 12)  # Produce random value 10-12 below the result
            l_than = int(result) + randint(10, 12)  # Produce random value 10-12 above the result

            # Block hint from being below MIN
            if g_than < 10:
                g_than = 10 + randint(randint(0, 2), randint(4, 6))     # Jack those randoms up

            # Block hint from being above MAX
            if l_than > 99:
                l_than = 99 - randint(randint(0, 2), randint(4, 6))     # Jeck dem randerms erp

            # --------------

            if guess < result:
                print(f"You sense the answer is greater than {guess} and less than {l_than}.")
            elif guess > result:    # Change to 'else'?
                print(f"You sense the answer is greater than {g_than} and less than {guess}.")

        # ==== CALL FOR HINT ====
        def hint_fetch():
            i = randint(0, 2)
            if i == 0:
                hint_sum()
            elif i == 1:
                hint_int()
            elif i == 2:        # Change to 'else'?
                hint_range()

        # Needs error handling for non-numeric input
        guess = input("Enter a number between 10 and 99: ")

        # == Successful attempt ==
        if int(guess) == int(result):
            if int(guess) and int(result) == 43:
                # == Dialogue for 43 win ==
                print("...")
                time.sleep(1.5)
                print(".......")
                time.sleep(2.5)
                print("Your attempt was successful. The sturdy pyxis emits a soft glow.")
                time.sleep(1)
                print("Although, a sudden cold chill runs down your spine...")
                time.sleep(2.5)
                print("...and you hear the faint sound of bells chiming in the distance.")
                time.sleep(3)
                print("Looking down at the chest, you hear a dull click as it pops open...")
                time.sleep(3)
                break
            else:
                # == Dialogue for regular win ==
                print("Your attempt was successful. The sturdy pyxis emits a soft glow.")
                time.sleep(2)
                print("A subtle warmth fills your palms.")
                time.sleep(1)
                print("You hear a click, and the chest pops open...")
                time.sleep(3)
                break

        # == Unsuccessful attempt ==
        elif int(guess) != int(result):
            attempts += 1
            if attempts in range(1, 4):
                print("The pyxis gently rattles in your hand.")
                time.sleep(1.5)
                hint_fetch()  # Call to retrieve random hint

            elif attempts == 4:
                print("The pyxis tremors with a strong vibration...")
                time.sleep(1.5)
                hint_fetch()  # Call to retrieve random hint


    if attempts == 5:
        # == Dialogue for 43 loss ==
        if result == 43:
            print("You have exceeded your allotted attempts. The correct answer was...")
            time.sleep(2.5)
            print(f"...the correct answer was {result}.")
            time.sleep(1.5)
            print("Your fingers start to grow cold, and your hands tremble.")
            time.sleep(1.5)
            print("Your vision blurs, as you feel something caught in your throat...")
            time.sleep(1.5)
            print("You seem to have forgotten what you were just doing, and return"
                  " to your travels...")
            time.sleep(3)
        else:
            # == Dialogue for regular loss ==
            print(f"You have exceeded your allotted attempts. The correct answer was {result}.")
            time.sleep(3)
            print("The sturdy pyxis slowly vanishes in front of your eyes...")
            time.sleep(1.5)
            print("You seem to have forgotten what you were just doing, and return"
                  " to your travels...")
            time.sleep(3)


if __name__ == '__main__':
    main()