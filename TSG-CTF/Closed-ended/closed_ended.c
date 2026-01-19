#include <unistd.h>
#include <sys/mman.h>
#include <stdio.h>

int main() {
    void* addr;
    char buf[10];

    mprotect((void*)0x401000, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC);

    if (close(1) != 0 || scanf("%p", &addr) != 1)
        return 0;

    if ((unsigned long)addr < 0x4010a7 || (unsigned long)addr > 0x402000) 
        return 0;

    if (scanf("%*c%c", (char*)addr) != 1)
        return 0;

    mprotect((void*)0x401000, 0x1000, PROT_READ | PROT_EXEC);

    scanf("%100s", buf);
    return 0;
}
