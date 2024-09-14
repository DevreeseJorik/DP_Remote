#include "packets.h"

void handlePackets() {
    HTTP_PACKET *rcvPacketHTTP = RCV_PACKET_BUFF_ADDRESS;
    PACKET *rcvPacket = &rcvPacketHTTP->packet;

    u32 result;
    while (TRUE) {
        result = downloadPacket(rcvPacketHTTP);
        switch (result) {
            case 1:
                handlePacket(rcvPacket);
                if (!rcvPacket->header.requestNext)
            return;
            default:
                break;
        }
    }
}

static inline u32 downloadPacket(HTTP_PACKET *packet) {
    fetchPacket(packet);
    return handleAsync();
}

static inline u32 uploadPacket(PACKET *packet) {
    sendPacket(packet);
    return handleAsync();
}

static inline u32 handleAsync() {
    while (TRUE) {
        tryAsyncUpdate();
        if (isAsyncComplete())
            break;
    }
    return getAsyncResult();
}

BOOL handlePacket(PACKET *packet) { 
    switch (packet->header.packetType){
        case TYPE_NONE:
            return FALSE;
        case TYPE_DATA_PACKET:
            return handleDataPacket((DATA_PACKET*)packet);
        case TYPE_CODE_PACKET:
            return handleCodePacket((CODE_PACKET*)packet);
        default:
            return FALSE;
    }
}

BOOL handleDataPacket(DATA_PACKET *packet) {
    if (packet->header.destinationAddress == NULL)
        return FALSE;

    memcp(packet->header.destinationAddress, packet->data, packet->header.size);
    return TRUE;
}

BOOL handleCodePacket(CODE_PACKET *packet) {
    return fp_thumb(packet->data, BOOL, ())();
}
    return TRUE;
}