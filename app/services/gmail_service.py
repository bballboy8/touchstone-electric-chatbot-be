from logging_module import logger
import traceback
from thirdparty.gmail_service import GmailAPIService



async def get_unread_emails_service():
    logger.debug("Inside Get Unread Emails Service")
    try:
        gmail_client = GmailAPIService()
        response = await gmail_client.get_unread_emails()
        print(response)
        return {"response": "Unread Emails Fetched Successfully", "status_code": 200}
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Exception in Get Unread Emails Service: {str(e)}")
        return {"response": "Internal Server Error", "status_code": 500}