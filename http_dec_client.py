import requests, sys, os, json
import app_dec_client
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    if len(sys.argv) == 2 and os.path.exists(sys.argv[1]):
        data = app_dec_client.decodeFile(sys.argv[1])
        response = requests.post( os.getenv('HTTP_SERVER'), 
                                 auth=(os.getenv('HTTP_SERVER_USERNAME'), os.getenv('HTTP_SERVER_PASSWORD')), 
                                 headers={"Content-Type": "application/json"}, data=data)
        if response.status_code == 200:
            print("ok:", response.json())
        else:
            print("failed:", response.status_code, response.text)
    else:
        print("arguments missing: source")
