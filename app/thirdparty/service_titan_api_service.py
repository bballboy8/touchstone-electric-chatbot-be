from config import constants
import requests


class ServiceTitanApiService:
    def __init__(self):
        self.client_id = constants.SERVICE_TITAN_CLIENT_ID
        self.client_secret = constants.SERVICE_TITAN_CLIENT_SECRET
        self.auth_url = constants.SERVICE_TITAN_BASE_AUTH_URL
        self.api_url = constants.SERVICE_TITAN_BASE_API_URL
        self.app_key = constants.SERVICE_TITAN_APP_KEY
        self.tenant_id = constants.SERVICE_TITAN_TENANT_ID

    async def _get_access_token(self):
        try:
            url = f"{self.auth_url}/connect/token"
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

    async def get_employees(self, page: int, page_size: int):
        try:
            response = await self._get_access_token()
            if response["status_code"] != 200:
                return response
            access_token = response["data"]["access_token"]
            url = f"{self.api_url}/settings/v2/tenant/{self.tenant_id}/employees?Page={page}&PageSize={page_size}"
            headers = {
                "Authorization": access_token,
                "ST-App-Key": self.app_key,
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return {"status_code": 200, "data": response.json()}
        except Exception as e:
            return {"status_code": 500, "data": f"Internal server error: {e}"}

    async def get_customers(self, page: int, page_size: int):
        try:
            response = await self._get_access_token()
            if response["status_code"] != 200:
                return response
            access_token = response["data"]["access_token"]
            url = f"{self.api_url}/crm/v2/tenant/{self.tenant_id}/customers?Page={page}&PageSize={page_size}"
            headers = {
                "Authorization": access_token,
                "ST-App-Key": self.app_key,
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return {"status_code": 200, "data": response.json()}
        except Exception as e:
            return {"status_code": 500, "data": f"Internal server error: {e}"}
