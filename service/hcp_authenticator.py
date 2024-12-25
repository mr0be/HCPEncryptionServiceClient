import requests

class HcpAuthenticator:

    def __init__(self, tokenUrl : str, clientId : str, clientSecret: str) -> None:
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.tokenUrl = tokenUrl
    

    def getAccessToken(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "client_id": self.clientId,
            "client_secret": self.clientSecret,
            "grant_type": "client_credentials",
            "audience": "https://api.hashicorp.cloud",
        }

        response = requests.post(self.tokenUrl, headers=headers, data=data)
        response.raise_for_status() 

        access_token = response.json().get("access_token")
        if not access_token:
            raise ValueError("Failed to retrieve access token")
        return access_token