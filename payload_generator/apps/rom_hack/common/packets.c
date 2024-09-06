#include "packets.h"

void handlePackets() {
    PACKET *packetBuf = PACKET_BUFF_ADDRESS;
    while (TRUE) {
        fetchPacket(packetBuf);
        handlePacket(packetBuf);

        if (!packetBuf->header.requestNext)
            return;
    }
}

BOOL handlePacket(PACKET *packet) { 
    switch (packet->header.packetType){
        case TYPE_DATA_PACKET:
            return handleDataPacket((DATA_PACKET*)packet);
        case TYPE_CODE_PACKET:
            return handleCodePacket((CODE_PACKET*)packet);
        default:
            return FALSE;
    }

    return TRUE;
}

BOOL handleDataPacket(DATA_PACKET *packet) {
    if (packet->header.destinationAddress == NULL)
        return FALSE;

    memcp(packet->header.destinationAddress, packet->data, packet->header.size);
    return TRUE;
}

BOOL handleCodePacket(CODE_PACKET *packet) {
    void (*func)() = (void (*)())packet->data;
    func();
    
    return TRUE;
}