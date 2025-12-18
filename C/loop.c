#include <stdio.h>

int main()
{
	int i = 100;
	int j = 400;

	while (i < j) {
		printf("%i\n", i);
		i = 2 * i;
	}
}
