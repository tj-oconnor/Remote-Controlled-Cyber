#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
	printf("Usage: ./pin <pin>\n");
	return 0;
    }

    if(atoi(argv[1]) == 1989) {
        printf("Correct! The password is: cQleZF\n");
    }
    else {
	printf("Incorrect\n");
    }
    return 0;
}
