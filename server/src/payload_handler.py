from .loghandler import LogHandler
import logging
from time import sleep

payload_logging = LogHandler('payload_generator', 'payloads.log', level=logging.INFO).get_logger()

class PayloadHandler():
    def __init__(self, payload_length=292):
        self._payload_length = payload_length

    def set_payload_length(self, length):
        self._payload_length = length

    def get_payload(self):
        try:
            choice = input("Path to the payload file: ")
            with open(choice, 'rb') as f:
                resp = f.read()
                resp = resp.ljust(self._payload_length, b'\x00')
                return resp
        except FileNotFoundError:
            payload_logging.error(f"Payload file {choice} not found.")
            resp = b'\x01\x00\xa0\xe3\x10\x80\xbd\xe8'
            resp += b'\x00' * (self._payload_length - len(resp))
            return resp
        
    def handle_post(self, data):
        pass

DUMP_ADDRESS = 0x02000000

class DumpPayloadHandler(PayloadHandler):
    def __init__(self, payload_length=292):
        super().__init__(payload_length)
        self._setup_file_path = r"./payload_generator/out/bin/rom_hack.bin"
        self._has_sent_setup = True
        self._packet_index = 0

        self._dump_file = r"./memory_dump.bin"
        with open(self._dump_file, 'wb') as f:
            f.write(b'')

    def get_payload(self):
        global DUMP_ADDRESS
        try:
            sleep(2)
            if not self._has_sent_setup:
                with open(self._setup_file_path, 'rb') as f:
                    resp = f.read()
                    resp = resp.ljust(self._payload_length, b'\x00')
                    self._has_sent_setup = True
                    return resp
            else:
                resp = b'\x03' # Packet type: Dump data
                if DUMP_ADDRESS + self._payload_length >= 0x23A8000:
                    resp += b'\x00'
                else:
                    resp += b'\x01' # Request another packet after this one
                resp += b'\x00' * 2 # Padding
                resp += self._packet_index.to_bytes(4, byteorder='little') # Packet index
                resp += DUMP_ADDRESS.to_bytes(4, byteorder='little') # Address
                resp += b'\x00' * (self._payload_length - len(resp))

                return resp
        except FileNotFoundError:
            payload_logging.error(f"Payload file not found. Did you run make?")
            resp = b'\x01\x00\xa0\xe3\x10\x80\xbd\xe8'
            resp += b'\x00' * (self._payload_length - len(resp))
            return resp
        
    def handle_post(self, data):
        global DUMP_ADDRESS
        with open(self._dump_file, 'ab') as f:
            f.write(data)
        
        DUMP_ADDRESS += 0xEC