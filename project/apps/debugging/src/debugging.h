#ifndef _DEBUGGING_H
#define _DEBUGGING_H

#include "common.h"
#include "functions.h"
#include <stdint.h>

inline static void write_byte(u32 addr, u8 value) {
    *(u8*)addr = value;
}

inline static void write_halfword(u32 addr, u16 value) {
    *(u16*)addr = value;
}

inline static void write_word(u32 addr, u32 value) {
    *(u32*)addr = value;
}

inline static void disableGIDCheck() {
    write_byte(0x0203386a, 0x00);
}

// inline static void setDotArtistToGTSProc() {
//     u32 base_address = 0x02106FC0;
//     u32* base_pointer = (u32*)(*(u32*)base_address);
//     u32* dot_artist = (u32*)((u8*)base_pointer + 0x138A);
    
//     u16 command_data[6] = {
//         0x28, 0x8000, 0x0,
//         0xB3, 0x8000, 0x2,
//     };

//     ((u16*)dot_artist)[0] = command_data[0];
//     ((u16*)dot_artist)[1] = command_data[1];
//     ((u16*)dot_artist)[2] = command_data[2];

//     // copy the next 3 commands 3 times
//     ((u16*)dot_artist)[3] = command_data[3];
//     ((u16*)dot_artist)[4] = command_data[4];

//     ((u16*)dot_artist)[6] = command_data[3];
//     ((u16*)dot_artist)[7] = command_data[4];

//     ((u16*)dot_artist)[9] = command_data[3];
//     ((u16*)dot_artist)[10] = command_data[4];

// }

static u8 command_data[40] __attribute__((section(".data.command_data"))) = {
    0x00, 0x00, 0x00, 0x00, // padding
    0xBD, 0x00, 0xB2, 0x02, 0xB3, 0x00, 0x0C, 0x80, 0x29, 0x00, 
    0x04, 0x80, 0x0C, 0x80, 0xB2, 0x00, 0x04, 0x80, 0x0C, 0x80, 
    0xA1, 0x00, 0xBC, 0x00, 0x06, 0x00, 0x01, 0x00, 0x01, 0x00, 
    0x00, 0x00, 0xBD, 0x00, 0x02, 0x00
};

void setDotArtistToGTSProc() {
    u32 base_address = 0x02106FC0;
    u32* base_pointer = (u32*)(*(u32*)base_address);
    u32* dot_artist = (u32*)((u8*)base_pointer + 0x138A);

    const uint8_t* command_pointer;

    __asm__ volatile (
        "mov %0, pc\n"
        "add %0, #0x18\n"
        : "=r" (command_pointer)
        : "r" (&command_data)
        : "memory"
    );

    memcp(command_pointer,dot_artist, sizeof(command_data) + 10);
}

#endif // _DEBUGGING_H