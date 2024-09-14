#ifndef _PACKETS_H
#define _PACKETS_H

#include "common.h"
#include "functions.h"

#ifndef PACKET_SIZE // PACKET_SIZE may be modified
#define PACKET_SIZE  292
#endif

enum {
    TYPE_NONE,
    TYPE_DATA_PACKET,    // copy to some destination
    TYPE_CODE_PACKET,    // execute on receive
};

typedef struct {
    u8 packetType;
	u8 requestNext;
	u16 padding;
    u32 packetId;
} PACKET_HEADER;

typedef struct {
    PACKET_HEADER header;
    u8 data[ PACKET_SIZE - sizeof(PACKET_HEADER)];
} PACKET;

typedef struct {
	u8 http_header[0xD4];
	PACKET packet;
} HTTP_PACKET;

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
#define RCV_PACKET_BUFF_ADDRESS (HTTP_PACKET *) 0x23B0000

static inline void fetchPacket(HTTP_PACKET *packet) { fetchPokemonResult(packet); }
static inline void sendPacket(PACKET *packet) { sendPokemonResult(packet); }
static inline u32 downloadPacket(HTTP_PACKET *packet);
static inline u32 uploadPacket(PACKET *packet);
static inline u32 handleAsync();

void handlePackets();
BOOL handlePacket(PACKET *packet);
BOOL handleDataPacket(DATA_PACKET *packet);
BOOL handleCodePacket(CODE_PACKET *packet);

#endif // _PACKETS_H