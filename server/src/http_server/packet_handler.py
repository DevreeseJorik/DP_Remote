import abc
import os
import yaml
import json
import logging

from time import sleep

from ..log_handler.log_handler import LogHandler

packet_logging = LogHandler('packet_handler', 'network.log', level=logging.DEBUG).get_logger()

class PacketGenerator(abc.ABC):
    def __init__(self, filepath, packet_type, bin_size):
        self.filepath = filepath
        self.packet_type = packet_type
        self.bin_size = bin_size
        self.bin_memory = bytearray(bin_size)

    def write_u8(self, value, address):
        self.bin_memory[address] = value & 0xFF
        return 1

    def write_u16(self, value, address, little_endian=True):
        assert address % 2 == 0, "Address must be even for 16-bit write."
        byte_order = 'little' if little_endian else 'big'
        self.bin_memory[address:address+2] = value.to_bytes(2, byte_order)
        return 2

    def write_u32(self, value, address, little_endian=True):
        assert address % 4 == 0, "Address must be a multiple of 4 for 32-bit write."
        byte_order = 'little' if little_endian else 'big'
        self.bin_memory[address:address+4] = value.to_bytes(4, byte_order)
        return 4

    def create_header(self, packet_id, request_next):
        index = 0
        index += self.write_u8(self.packet_type, index)
        index += self.write_u8(request_next, index)
        index += self.write_u16(0, index) # padding
        index += self.write_u32(packet_id, index)
        return index

    @abc.abstractmethod
    def generate_packet(self, packet_id, request_next):
        pass

    def write_packet(self):
        assert len(self.bin_memory) == self.bin_size
        with open(f"packet_{os.path.basename(self.filepath)}", 'wb') as f:
            f.write(self.bin_memory)

class DefaultPacketGenerator(PacketGenerator):
    def __init__(self, packet_info, bin_size):
        super().__init__(packet_info.get("filepath"), packet_info.get("id"), bin_size)

    def generate_packet(self, packet_id, request_next):
        with open(self.filepath, 'rb') as f:
            data = f.read()

        index = 0
        self.bin_memory[index:index + len(data)] = data
        return self.bin_memory

class DataPacketGenerator(PacketGenerator):
    def __init__(self, packet_info, bin_size):
        super().__init__(packet_info.get("filepath"), packet_info.get("id"), bin_size)
        self.destination_address = packet_info.get("address", 0x0)

    def create_header(self, packet_id, request_next, size):
        index = super().create_header(packet_id, request_next)
        index += self.write_u32(self.destination_address, index)
        index += self.write_u32(size, index)
        return index

    def generate_packet(self, packet_id, request_next):
        with open(self.filepath, 'rb') as f:
            data = f.read()

        index = self.create_header(packet_id, request_next, len(data))
        assert len(data) <= self.bin_size - index

        self.bin_memory[index:index+len(data)] = data
        return self.bin_memory

class CodePacketGenerator(PacketGenerator):
    def __init__(self, packet_info, bin_size):
        super().__init__(packet_info.get("filepath"), packet_info.get("id"), bin_size)

    def generate_packet(self, packet_id, request_next):
        with open(self.filepath, 'rb') as f:
            data = f.read()

        index = self.create_header(packet_id, request_next)
        self.bin_memory[index:index+len(data)] = data
        return self.bin_memory

class DumpPacketGenerator(PacketGenerator):
    def __init__(self, packet_info, bin_size):
        super().__init__(packet_info.get("filepath"), packet_info.get("id"), bin_size)
        self.dump_address = packet_info.get("address", 0x0)
        self.dump_size = packet_info.get("size", 0x0)

    def create_header(self, packet_id, request_next):
        index = super().create_header(packet_id, request_next)
        index += self.write_u32(self.dump_address, index)
        index += self.write_u32(self.dump_size, index)
        return index

    def generate_packet(self, packet_id, request_next):
        self.create_header(packet_id, request_next)
        return self.bin_memory

class PacketHandler:
    def __init__(self, config_path, payload_length=292):
        self.packet_id = 0
        self.payload_length = payload_length
        self.generators = {
            "default": { "class": DefaultPacketGenerator, "id": 0},
            "data": { "class": DataPacketGenerator, "id": 1},
            "code": { "class": CodePacketGenerator, "id": 2},
            "dump": { "class": DumpPacketGenerator, "id": 3},
        }

        self.config = self.load_config(config_path)
        self.payload_id = 0

    def load_config(self, config_path):
        _, ext = os.path.splitext(config_path)
        ext = ext.lower()

        if ext in ['.yaml', '.yml']:
            with open(config_path, 'r') as f:
                config_data = yaml.safe_load(f)
                return config_data
        elif ext in ['.json']:
            with open(config_path, 'r') as f:
                config_data = json.load(f)
                return config_data
            
        packet_logging.error(f"Unsupported configuration file: {config_path}. Use .yaml or .json.")
        return []

    def reset(self):
        packet_logging.debug("Resetting packet handler.")
        self.payload_id = 0

    def _update(self, data):
        if data is None: 
            return 
        
        self.payload_length = data.get("payload_length", self.payload_length)

    def get_payload(self):
        sleep(2)
        packet_config =  self.config.get("packets", [])
        if self.payload_id >= len(packet_config):
            timeout = self.config.get("out_of_packets_timeout", 10)
            packet_logging.info(f"Got request but all payloads have been sent. Timeout: {timeout}s.")
            sleep(timeout)
            return b'\x00' * self.payload_length
        
        packet_info = packet_config[self.payload_id]

        packet_type = packet_info.get("packet_type")
        generator_info =  self.generators.get(packet_type, self.generators.get("default"))
        packet_info["id"] = generator_info.get("id")
        generator = generator_info.get("class")(packet_info, self.payload_length)

        self._update(packet_info.get("pre_update"))
        request_next = int(self.payload_id != (len(packet_config) -1))
        data = generator.generate_packet(self.packet_id, request_next)
 
        self._update(packet_info.get("post_update"))

        # TODO: payload_id should only be incremented when acknowledged by client 
        self.packet_id += 1
        self.payload_id += 1 

        return bytes(data)
    
    def handle_post(self, data):
        pass