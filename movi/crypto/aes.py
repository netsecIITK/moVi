"""
Handles the logic of encrypting and decrypting
frame data
"""


class Aes:
    def __init__(self, key):
        self.key = key

    def sign(self, data):
        return self.key.encode()

    def check_sign(self, enc_sign, enc_data):
        if enc_sign == self.sign(enc_data):
            return True
        else:
            return False
