from logging_module import logger
from thirdparty.vonage_service import VonageApi
from thirdparty.openai_service import convert_to_est
from db_connection import db
from config import constants
from datetime import datetime
from datetime import timedelta
import time
import pytz


async def send_test_campaign_sms(to, text):
    try:
        vonage_api = VonageApi()
        response = vonage_api.send_sms(to, text)
        if response["status_code"] != 200:
            return {"status_code": 500, "data": response["data"]}

        return {
            "status_code": 200,
            "data": f"SMS Sent Successfully to {to} with message id: {response['data']}",
        }
    except Exception as e:
        logger.error(f"Error in send_test_sms: {e}")
        return {"status_code": 500, "data": f"Internal Server Error: {e}"}