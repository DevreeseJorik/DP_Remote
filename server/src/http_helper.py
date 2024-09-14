from base64 import b64decode

class B64SCCrypto():
    def decrypt(self, data):
        b64_decoded = self.b64decode(data)
        sc_decoded = self.sce_decrypt(b64_decoded)
        return sc_decoded

    def b64decode(self, data):
        return b64decode(data.replace('-', '+').replace('_', '/'))
    
    def sce_decrypt(self, data):
        checksum = int.from_bytes(data[:4], byteorder='big') ^ 0x4a3b2c1d
        return self.decrypt_sce_data(data[4:244], checksum | (checksum << 16))[4:]
    
    def decrypt_sce_data(self, encrypted_data, state):
        decrypted_data = bytearray()
        for byte in encrypted_data:
            state = (state * 0x45 + 0x1111) & 0x7fffffff
            keybyte = (state >> 16) & 0xff
            decrypted_data.append((byte ^ keybyte) & 0xff)
        return decrypted_data
        