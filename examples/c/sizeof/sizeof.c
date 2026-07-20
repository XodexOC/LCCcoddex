#include <stdio.h>
#include <stddef.h>
int main(void){
  printf("int=%zu long=%zu size_t=%zu char=%zu\n", sizeof(int), sizeof(long), sizeof(size_t), sizeof(char));
  return 0;
}
