from config import constants
import requests
from models.service_titan import ServiceTitanCustomer, ServiceTitanBookingRequest
import json
import uuid
import httpx
from tenacity import retry, wait_fixed, stop_after_attempt
from logging_module import logger

class ServiceTitanApiService:
    def __init__(self):
        self.client_id = constants.SERVICE_TITAN_CLIENT_ID
        self.client_secret = constants.SERVICE_TITAN_CLIENT_SECRET
        self.auth_url = constants.SERVICE_TITAN_BASE_AUTH_URL
        self.api_url = constants.SERVICE_TITAN_BASE_API_URL
        self.app_key = constants.SERVICE_TITAN_APP_KEY
        self.tenant_id = constants.SERVICE_TITAN_TENANT_ID
        self.booking_provider_id = constants.SERVICE_TITAN_BOOKING_PROVIDER_ID

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

    async def health_check(self):
        try:
            response = await self._get_access_token()
            response["client_id"] = self.client_id
            response["api_url"] = self.api_url
            response["auth_url"] = self.auth_url
            if response["status_code"] != 200:
                return response
            return {
                "response": response,
                "message": "Service Titan API service is working correctly.",
                "status_code": 200,
            }
        except Exception as e:
            return {
                "message": f"An error occurred while testing the Service Titan API service: {e}",
                "status_code": 500,
            }

    async def get_jobs(self, page: int, page_size: int):
        try:
            response = await self._get_access_token()
            if response["status_code"] != 200:
                return response
            access_token = response["data"]["access_token"]
            url = f"{self.api_url}/jpm/v2/tenant/{self.tenant_id}/jobs?Page={page}&PageSize={page_size}"
            headers = {
                "Authorization": access_token,
                "ST-App-Key": self.app_key,
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return {"status_code": 200, "data": response.json()}
        except Exception as e:
            return {"status_code": 500, "data": f"Internal server error: {e}"}

    async def get_job_by_id(self, job_id: int):
        try:
            response = await self._get_access_token()
            if response["status_code"] != 200:
                return response
            access_token = response["data"]["access_token"]
            url = f"{self.api_url}/jpm/v2/tenant/{self.tenant_id}/jobs/{job_id}"
            headers = {
                "Authorization": access_token,
                "ST-App-Key": self.app_key,
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return {"status_code": 200, "data": response.json()}
        except Exception as e:
            return {"status_code": 500, "data": f"Internal server error: {e}"}

    async def get_locations(self, page: int, page_size: int):
        try:
            response = await self._get_access_token()
            if response["status_code"] != 200:
                return response
            access_token = response["data"]["access_token"]
            url = f"{self.api_url}/crm/v2/tenant/{self.tenant_id}/locations?Page={page}&PageSize={page_size}"
            headers = {
                "Authorization": access_token,
                "ST-App-Key": self.app_key,
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return {"status_code": 200, "data": response.json()}
        except Exception as e:
            return {"status_code": 500, "data": f"Internal server error: {e}"}

    async def get_location_by_id(self, location_id: int):
        try:
            response = await self._get_access_token()
            if response["status_code"] != 200:
                return response
            access_token = response["data"]["access_token"]
            url = (
                f"{self.api_url}/crm/v2/tenant/{self.tenant_id}/locations/{location_id}"
            )
            headers = {
                "Authorization": access_token,
                "ST-App-Key": self.app_key,
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return {"status_code": 200, "data": response.json()}
        except Exception as e:
            return {"status_code": 500, "data": f"Internal server error: {e}"}

    async def create_customer(self, customer_data: ServiceTitanCustomer):
        try:
            response = await self._get_access_token()
            if response["status_code"] != 200:
                return response
            access_token = response["data"]["access_token"]
            url = f"{self.api_url}/crm/v2/tenant/{self.tenant_id}/customers"
            headers = {
                "Authorization": access_token,
                "ST-App-Key": self.app_key,
            }
            data = customer_data.model_dump()
            response = requests.post(url, headers=headers, json=data)
            if response.status_code != 200:
                return {
                    "status_code": response.status_code,
                    "data": json.loads(response.text),
                }
            response.raise_for_status()
            return {"status_code": 200, "data": response.json()}
        except Exception as e:
            return {"status_code": 500, "data": f"Internal server error: {e}"}

    async def get_customer_by_id(self, customer_id: int):
        try:
            response = await self._get_access_token()
            if response["status_code"] != 200:
                return response
            access_token = response["data"]["access_token"]
            url = (
                f"{self.api_url}/crm/v2/tenant/{self.tenant_id}/customers/{customer_id}"
            )
            headers = {
                "Authorization": access_token,
                "ST-App-Key": self.app_key,
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return {"status_code": 200, "data": response.json()}
        except Exception as e:
            return {"status_code": 500, "data": f"Internal server error: {e}"}
        

    async def create_booking(self, booking_data: ServiceTitanBookingRequest, conversation_summary: str = None):
        try:
            """
                {
                "source": "online",
                "name": "Ai Customer 4",
                "summary": "Patch Work",
                "isFirstTimeClient": true,
                "contacts": [{"type": "MobilePhone", "value": "+919993227728"}]
                }
            """
            response = await self._get_access_token()
            if response["status_code"] != 200:
                return response
            access_token = response["data"]["access_token"]
            url = f"{self.api_url}/crm/v2/tenant/{self.tenant_id}/booking-provider/{self.booking_provider_id}/bookings"

            headers = {
                "Authorization": access_token,
                "ST-App-Key": self.app_key,
            }
            data = booking_data.model_dump()
            data["externalId"] = str(uuid.uuid4())
            data["summary"] = conversation_summary if conversation_summary else "Booking Request"         

            print(data, "service titand booking request")
            response = requests.post(url, headers=headers, json=data)
            if response.status_code != 200:
                return {
                    "status_code": response.status_code,
                    "data": json.loads(response.text),
                }
            response.raise_for_status()
            return {"status_code": 200, "data": response.json()}
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"status_code": 500, "data": f"Internal server error: {e}"}

    async def get_customer_contacts_by_name(self, name:str):
        try:
            response = await self._get_access_token()
            if response["status_code"] != 200:
                return response
            access_token = response["data"]["access_token"]
            url = f"{self.api_url}/crm/v2/tenant/{self.tenant_id}/contacts?title={name}"
            headers = {
                "Authorization": access_token,
                "ST-App-Key": self.app_key,
            }
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                return {
                    "status_code": response.status_code,
                    "data": json.loads(response.text),
                }
            response.raise_for_status()
            return {"status_code": 200, "data": response.json()}
        except Exception as e:
            return {"status_code": 500, "data": f"Internal server error: {e}"}
        
    async def create_contact(self, name: str):
        try:
            response = await self._get_access_token()
            if response["status_code"] != 200:
                return response
            access_token = response["data"]["access_token"]
            url = f"{self.api_url}/crm/v2/tenant/{self.tenant_id}/contacts"
            headers = {
                "Authorization": access_token,
                "ST-App-Key": self.app_key,
            }
            data = {"title": name}
            response = requests.post(url, headers=headers, json=data)
            if response.status_code != 200:
                return {
                    "status_code": response.status_code,
                    "data": json.loads(response.text),
                }
            response.raise_for_status()
            return {"status_code": 200, "data": response.json()}
        except Exception as e:
            return {"status_code": 500, "data": f"Internal server error: {e}"}