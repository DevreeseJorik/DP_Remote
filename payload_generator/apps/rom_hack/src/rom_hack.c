#include "rom_hack.h"

__attribute__((naked))
__attribute__((section(".text.main")))
void main(void) {
    __asm__ volatile (
        "pop {r4, pc}\n"      // Ensure pop {r4, pc} for return
    );
}