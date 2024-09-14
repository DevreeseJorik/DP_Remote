from .loghandler import LogHandler
import logging

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