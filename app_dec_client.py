import os, base64, sys
from helper.decrypt import DecryptHelper
from service.hcp_client import HcpClient
from service.hcp_authenticator import HcpAuthenticator

from dotenv import load_dotenv

load_dotenv()
hcpClient = HcpClient(
                HcpAuthenticator(
                os.getenv('HIC_AUTH_URL'),os.getenv('HIC_CLIENT_ID'),os.getenv('HIC_CLIENT_SECRET')),
                os.getenv('HIC_SECRET_URL')
            )


def decodeFile(encodedFile: str) -> str:
        secrect64base = hcpClient.getSecrect4Key(
            os.getenv('HIC_ORGANIZATION_ID'),
            os.getenv('HIC_PROJECT_ID'),
            os.getenv('HIC_APP_NAME'),
            "client_key"
        )
        secrect = base64.b64decode(secrect64base)
        decryptHelper = DecryptHelper(secrect)
        return decryptHelper.decrypt_file(encodedFile)
    

if __name__ == "__main__":
    if len(sys.argv) == 3 and os.path.exists(sys.argv[1]):
        decrypted_data = decodeFile(sys.argv[1])
        with open(sys.argv[2], "wb") as f:
            f.write(decrypted_data)
    else:
        print("arguments missing: source target")