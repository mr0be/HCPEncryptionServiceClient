import os, base64
from helper.encrypt import EncryptHelper
from helper.generate_rsa_key import RSAGenerator
from dotenv import load_dotenv
from service.hcp_authenticator import HcpAuthenticator
from service.hcp_client import HcpClient 
import sys

load_dotenv()
hcpClient = HcpClient(
                HcpAuthenticator(
                os.getenv('HIC_AUTH_URL'),os.getenv('HIC_CLIENT_ID'),os.getenv('HIC_CLIENT_SECRET')),
                os.getenv('HIC_SECRET_URL')
            )



def generateRSAFiles() -> tuple:
    rSAGenerator = RSAGenerator("private_key.pem", "public_key.pem")
    rSAGenerator.generateRSAKeys()
    
    with open("private_key.pem", "rb") as private_key_file:
           private_key = private_key_file.read()

    with open("public_key.pem", "rb") as public_key_file:
           public_key = public_key_file.read()
  
    return private_key,public_key


def addSecret(keyname: str,private_key : bytes) -> bool:
    encoded_data = base64.b64encode(private_key)
    result = hcpClient.addSecret(
        os.getenv('HIC_ORGANIZATION_ID'),
        os.getenv('HIC_PROJECT_ID'),
        os.getenv('HIC_APP_NAME'),
        keyname,
        encoded_data.decode('utf-8')
    )
    return result
    


def encodeFile(file : str, publicKey : bytes) -> str:
    encryptHelper = EncryptHelper(publicKey)
    return encryptHelper.encryptFile(file)

if __name__ == "__main__":
     if len(sys.argv) == 3:
        private_key,public_key = generateRSAFiles()
        if addSecret("client_key",private_key) :
            resultFile = encodeFile(sys.argv[1],public_key)
            with open(sys.argv[2], "w") as f:
                f.write(resultFile)
     else:
          print("arguments missing: source target")
          
        
    


        

