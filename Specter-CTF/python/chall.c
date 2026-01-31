#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

char *gets(char*buf);
void win() {
    puts("You win!");
    puts("Flag: Sp3ctr3CTF{Th1s_1s_4_F4ls3_Fl49}");
    exit(0);
}


int main() {
    setvbuf(stdout, NULL, _IONBF, 0);

    char buf[65];

    puts("Input:");
    gets(buf);  
    puts("Done!");

    return 0;
}
