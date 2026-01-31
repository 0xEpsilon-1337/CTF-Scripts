#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void win() {

    execv("/bin/sh",NULL);
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);

    FILE *fp = stdout;
    if (!fp) {
        puts("fp failed");
        return 1;
    }

    puts("Welcome to IO training challenge!");
    puts("Send up to 256 bytes (overflow demo):");

    printf("stdout : %p\n",fp);

    ssize_t n = read(0, fp, 256);
   
  
    return 0;
}
