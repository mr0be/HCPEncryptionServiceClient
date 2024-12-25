from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import base64
import os


class DecryptHelper:
    def __init__(self, privateKey: bytes ):
        self.privateKey = privateKey

    def __load_private_key(self):
        return serialization.load_pem_private_key(self.privateKey, password=None)

    def decrypt_file(self,input_path : str) -> str:
        private_key = self.__load_private_key()
        decrypted_data = []

        with open(input_path, "r") as f:
            for line in f:
                encrypted_chunk = base64.b64decode(line.strip())
                decrypted_chunk = private_key.decrypt(
                    encrypted_chunk,
                    padding.PKCS1v15()
                )
                decrypted_data.append(decrypted_chunk)
        
        return b"".join(decrypted_data)