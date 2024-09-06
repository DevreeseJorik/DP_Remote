#ifndef _FUNCTIONS_H
#define _FUNCTIONS_H

#include "common.h"

#define fp_memcp 0x020e17b0
#define memcp(dest, src, n) ((void* (*) (void*, void*, u32))fp_memcp)(dest, src, n)

#define fp_fetchPokemonResult 0x02234E68
#define fetchPokemonResult(dest) ((void* (*) (void*))fp_fetchPokemonResult)(dest)

static inline void *memset(void *buf, u8 ch, u32 n)
{
    for(int i=0; i<n; i++)
    {
        ((u8*)buf)[i] = ch;
    }
    return buf;
}

#endif // _FUNCTIONS_H