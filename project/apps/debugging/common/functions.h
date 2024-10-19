#ifndef _FUNCTIONS_H
#define _FUNCTIONS_H

#include "common.h"
#include <stdint.h>

#define fp_arm(address, type, param) ((type (*) param)((uintptr_t)(address) & ~1))
#define fp_thumb(address, type, param) ((type (*) param)((uintptr_t)(address) | 1))

#define fp_memcp8 fp_arm(0x20CE3E0, void, (void*, void*, u32))
static inline void memcp(void* src, void* dest, u32 size) { fp_memcp8(src, dest, size);}

#endif // _FUNCTIONS_H