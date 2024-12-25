from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


class RSAGenerator:

    def __init__(self,privateKeyPath : str,publicKeyPath : str ) -> None:
        self.privateKeyPath = privateKeyPath
        self.publicKeyPath = publicKeyPath

    def generateRSAKeys(self) -> None:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        with open(self.privateKeyPath, "wb") as f:
            f.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                )
            )

        public_key = private_key.public_key()
        with open(self.publicKeyPath, "wb") as f:
            f.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
            )