from config import constants
import requests


class ServiceTitanApiService:
    def __init__(self):
        self.client_id = constants.SERVICE_TITAN_CLIENT_ID
        self.client_secret = constants.SERVICE_TITAN_CLIENT_SECRET
        self.api_url = constants.SERVICE_TITAN_BASE_API_URL

    def get_access_token(self):
        try:
            url = f"{self.api_url}/connect/token"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}

            payload = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }

            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            return {"status_code": 200, "data": response.json()}
        except Exception as e:
            return {"status_code": 500, "data": f"Internal server error:{e}"}
