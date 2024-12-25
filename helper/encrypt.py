from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
import base64

class EncryptHelper:
    def __init__(self, publicKey: bytes):
        self.publicKey = publicKey

    def __get_max_chunk_size(self, public_key : RSAPublicKey) -> int:
        key_size_in_bytes = public_key.key_size // 8
        padding_size = 11
        return key_size_in_bytes - padding_size

    def __load_public_key(self):
         return serialization.load_pem_public_key(self.publicKey)

    def encryptFile(self, input_path: str) -> str:
        public_key = self.__load_public_key()
        max_chunk_size = self.__get_max_chunk_size(public_key)
        encrypted_chunks = []

        with open(input_path, "rb") as f:
            while chunk := f.read(max_chunk_size):
                try:
                    encrypted_chunk = public_key.encrypt(
                        chunk,
                        padding.PKCS1v15()
                    )
                    encrypted_chunks.append(base64.b64encode(encrypted_chunk).decode("utf-8"))
                except Exception as e:
                    raise ValueError(f"Error while encrypting a chunk: {str(e)}")
        return "\n".join(encrypted_chunks)
