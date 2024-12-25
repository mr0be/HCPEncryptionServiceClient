from service.hcp_authenticator import HcpAuthenticator
import requests

class HcpClient:

    def __init__(self,hcpAuthenticator: HcpAuthenticator, baseUrl: str ) ->None:
        self.baseUrl = baseUrl
        self.hcpAuthenticator = hcpAuthenticator


    def __createRequestInfo(self, organizationId : str, projectId : str, appName: str) -> tuple:
        accessToken = self.hcpAuthenticator.getAccessToken()
        url = f"{self.baseUrl}/organizations/{organizationId}/projects/{projectId}/apps/{appName}"
        headers = {
            "Authorization": f"Bearer {accessToken}",
        }
        return url, headers


    def addSecret(self, organizationId : str, projectId : str, appName: str, keyname: str, value: str) -> bool:
        url , headers = self.__createRequestInfo(organizationId,projectId,appName)
        url = f'{url}/secret/kv'
        secret_data = {
                "name": keyname,
                "value": value
            }
        response = requests.post(url, json=secret_data, headers=headers)
        if response.status_code == 200:
            return True
        return False

    def getSecrect4Key(self, organizationId : str, projectId : str, appName: str, key: str) -> str | None:
        url , headers = self.__createRequestInfo(organizationId,projectId,appName)
        url = f'{url}/secrets:open'
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        for secret in result.get("secrets", []):
            if secret.get("name") == key:
                return secret.get("static_version", {}).get("value")
        return None