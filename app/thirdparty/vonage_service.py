from config import constants
from logging_module import logger
from vonage import Auth, Vonage
from vonage_messages.models import Sms


class VonageApi:
    def __init__(self):
        self.vonage_client = Vonage(
            Auth(
                application_id=constants.VONAGE_APPLICATION_ID,
                private_key="private.key",
            )
        )

    def send_sms(self, to, text):
        try:
            logger.info(f"Sending SMS to {to} with text: {text}")
            response = self.vonage_client.messages.send(
                Sms(
                    to=to,
                    from_=constants.VONAGE_FROM_NUMBER,
                    text=text,
                )
            )

            logger.info(f"Vonage SMS response: {response}")
            return {"status_code": 200, "data": response.message_uuid}
        except Exception as e:
            logger.error(f"Error in send_sms: {e}")
            return {"status_code": 500, "data": f"Internal Server Error: {e}"}
        
    def send_whatsapp_message(self, to, text):
        try:
            response = self.vonage_client.messages.send(
                Sms(
                    to=to,
                    from_=constants.VONAGE_FROM_NUMBER,
                    text=text,
                    channel="whatsapp",
                )
            )

            logger.info(f"Vonage WhatsApp response: {response}")
            return {"status_code": 200, "data": response.message_uuid}
        except Exception as e:
            logger.error(f"Error in send_whatsapp_message: {e}")
            return {"status_code": 500, "data": f"Internal Server Error: {e}"}
