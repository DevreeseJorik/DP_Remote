import sys
import os

class PacketGenerator:
    def __init__(self, payload_size=292):
        self.header = {
            "packetType": "u8",
            "requestNext": "u8",
	        "padding": "u16",
            "packetId": "u32"
        }
        self.payload_size = payload_size

    def load(self, file) -> str:
        with open(file, "rb") as f:
            return f.read()

    def set_payload_size(self, size):
        self.payload_size = size
    
    def convert(self, file, **args):
        data = self.load(file)
        

class DataPacketGenerator:
    def __init__(self):
        pass

    def convert(self, data, **args):

        pass

class CodePacketGenerator:
    def __init__(self):
        pass

    def convert(self, data, **args):
        pass

class DumpPacketGenerator:
    def __init__(self):
        pass

    def convert(self, data, **args):
        pass


class PacketManager:
    def generate(self) -> None:
        pass 
        
    def convert(self, packet_type, data, **args):
        


