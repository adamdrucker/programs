import random
import os

def main():

    def captcha():

        LOW_ALPHA = "abcdefghijklmnopqrstuvwxyz"
        CAP_ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        NUMS = "0123456789"
        
        captcha_list = []

        # Prints random selection from a data set
        for i in range(2):

            # Randomize seed each for each iteration
            random.seed(os.urandom(random.randint(0, 255)))

            # Append two random choices from each string to blank list
            captcha_list.append(random.choice(NUMS))
            captcha_list.append(random.choice(LOW_ALPHA))
            captcha_list.append(random.choice(CAP_ALPHA))

        random.shuffle(captcha_list)

        print(''.join(captcha_list))

    captcha()

main()


