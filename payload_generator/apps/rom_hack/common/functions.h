#ifndef _FUNCTIONS_H
#define _FUNCTIONS_H

#include "common.h"
#include <stdint.h>

#define fp_arm(address, type, param) ((type (*) param)((uintptr_t)(address) & ~1))
#define fp_thumb(address, type, param) ((type (*) param)((uintptr_t)(address) | 1))

#define fp_memcp8 fp_arm(0x20CE3E0, void, (void*, void*, u32))
static inline void memcp(void* dest, void* src, u32 size) { fp_memcp8(dest, src, size);}

#define fp_memset fp_arm(0x20CE34C, void, (void*, u8, u32))
static inline void memset(void* dest, u8 value, u32 size) { fp_memset(dest, value, size); }
#define fp_fetchPokemonResult fp_thumb(0x02234E68, u32, (void*))
static inline u32 fetchPokemonResult(void* rcv_buf) { return fp_fetchPokemonResult(rcv_buf); }

#endif // _FUNCTIONS_H