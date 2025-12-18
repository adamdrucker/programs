#include <stdio.h>

int main() {
    printf("hello, ");
    printf("world");
    printf("\n");

    printf("\"test 1\"\n");
    printf("\ttest 2 with a \ttab\t\n");
    printf("testing out the \bbackspace\n");
    /* \x prints the hex value of the characters
    that follow */
    printf("test 3 \x6e\x6f \n");
    printf("test 4 \a \n");
}
