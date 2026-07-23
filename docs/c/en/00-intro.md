# Lesson 00: Introduction to C

C is a general-purpose compiled language created in 1972 by Dennis Ritchie.
It forms the foundation of UNIX and most modern operating systems.

## First program

```c
#include <stdio.h>

int main(void) {
    printf("Hello, Xodex!\n");
    return 0;
}
```

### Compile and run

```bash
gcc hello.c -o hello
./hello
```
