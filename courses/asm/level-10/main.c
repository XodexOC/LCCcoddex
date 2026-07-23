#include <stdio.h>

extern int square(int x);

int main(void) {
    int x = 7;
    printf("%d^2 = %d\n", x, square(x));
    return 0;
}
