from logging_module import logger
from thirdparty.vonage_service import VonageApi
from thirdparty.openai_service import OpenAIService
from thirdparty.pinecone_service import PineConeDBService


async def send_test_sms(to, text):
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


async def inbound_sms(request):
    try:
        request = await request.json()

        vonage_api = VonageApi()
        openai_client = OpenAIService()
        pinecone_client = PineConeDBService()

        query = request["text"]

        channel = "sms"
        if "channel" in request:
            channel = request["channel"]

        to = request["msisdn"]

        response = await pinecone_client.query_data(query, 3, None)
        if response["status_code"] != 200:
            return response

        matches = response["response"]["matches"]
        context = " ".join([match["metadata"]["text"] for match in matches])

        response = await openai_client.generate_ai_agent_response(
            context=context, query=query
        )
        if response["status_code"] != 200:
            return response
        
        gpt_response = response["response"]

        if channel == "whatsapp":
            logger.info("Sending WhatsApp message")
            response = vonage_api.send_whatsapp_message(to, gpt_response)
            return response
        elif channel == "sms":
            logger.info("Sending SMS message")
            response = vonage_api.send_sms(to, gpt_response)
            return response
        
        logger.info("Returning from Inbound SMS service")
        return {"status_code": 200, "data": "Inbound SMS service"}
    except Exception as e:
        logger.error(f"Error in inbound_sms: {e}")
        return {"status_code": 500, "data": f"Internal Server Error: {e}"}


async def sms_status(request):
    try:
        request = await request.json()
        print(request)
        logger.info("Inside SMS Status service")
        return {"status_code": 200, "data": "SMS Status service"}
    except Exception as e:
        logger.error(f"Error in sms_status: {e}")
        return {"status_code": 500, "data": f"Internal Server Error: {e}"}
