#ifndef _PACKETS_H
#define _PACKETS_H

#include "common.h"
#include "functions.h"

#define PACKET_BUFF_ADDRESS (PACKET *) 0x23B8000

#ifndef PACKET_SIZE // PACKET_SIZE may be modified
#define PACKET_SIZE 292
#endif

#define fetchPacket fetchPokemonResult // use Pokemon result API as packet data

enum {
    TYPE_NONE,
    TYPE_DATA_PACKET,    // copy to some destination
    TYPE_CODE_PACKET,    // execute on receive
};

typedef struct {
    u8 packetType;
    u32 packetId;
    BOOL requestNext;
} PACKET_HEADER;

typedef struct {
    PACKET_HEADER header;
    u8 data[ PACKET_SIZE - sizeof(PACKET_HEADER)];
} PACKET;

typedef struct {
    PACKET_HEADER header;
    void *destinationAddress;
    u32 size;
} DATA_PACKET_HEADER;

typedef struct {
    DATA_PACKET_HEADER header;
    u8 data[ PACKET_SIZE - sizeof(DATA_PACKET_HEADER)];
} DATA_PACKET;

typedef struct {
    PACKET_HEADER header;
} CODE_PACKET_HEADER;

typedef struct {
    CODE_PACKET_HEADER header;
    u8 data[ PACKET_SIZE - sizeof(CODE_PACKET_HEADER)];
} CODE_PACKET;

void handlePackets();
BOOL handlePacket(PACKET *packet);
BOOL handleDataPacket(DATA_PACKET *packet);
BOOL handleDataPacket(DATA_PACKET *packet);
BOOL handleCodePacket(CODE_PACKET *packet);

#endif // _PACKETS_H