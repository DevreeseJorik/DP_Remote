#include "debugging.h"

__attribute__((naked))
__attribute__((section(".text.main")))
__attribute__((target("arm")))
void main(void) {
    __asm__ volatile (
        "add r0, pc, #0x1\n"
        "bx r0\n"
    );
}

__attribute__((naked))
__attribute__((section(".text.main_thumb")))
__attribute__((target("thumb")))
void main_thumb(void) {
    __asm__ volatile (
        "push {r1-r7}\n"
    );
    // disableGIDCheck();
    setDotArtistToGTSProc();
    __asm__ volatile (
        "pop {r1-r7}\n"
        "mov r0, #0x1\n"
        "pop {r4, pc}\n"
    );
}