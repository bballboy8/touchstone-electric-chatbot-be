from logging_module import logger
from thirdparty.vonage_service import VonageApi
from thirdparty.openai_service import OpenAIService, convert_to_est
from thirdparty.pinecone_service import PineConeDBService
from db_connection import db
from config import constants
from datetime import datetime
from datetime import timedelta
import time
from services import train_agent_service


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

async def db_output_formatter_to_openai_format(messages:list):
    try:
        formatted_data = []
        for message in messages:
            user_content = f"Message Timestamp in EST: {message['created_at']} \nMessage : {message['query']}"
            formatted_data.append(
                {
                    "role": "user", 
                    "content": [{"type": "text", "text": user_content}]
                }
            )
            formatted_data.append(
                {
                    "role": "assistant", 
                    "content": [{"type": "text", "text": message['response']}]
                }
            )
        return formatted_data
    except Exception as e:
        logger.error(f"Error in db_output_formatter_to_openai_format: {e}")
        return {"status_code": 500, "data": f"Internal Server Error: {e}"}


async def get_users_previous_messages_history_of_last_30_days(msisdn):
    try:
        vonage_webhooks_collection = db[constants.VONAGE_WEBHOOKS_COLLECTION]
        query = {"msisdn": msisdn, "created_at": {"$gte": datetime.now() - timedelta(days=30)}, "source": "inbound_sms"}
        history = await vonage_webhooks_collection.find(query, {'query':1, 'response':1, 'messageId':1, "_id":0, "created_at":1}).to_list(length=None)
        formatted_response = await db_output_formatter_to_openai_format(list(history))
        return {"status_code": 200, "data": formatted_response}
    except Exception as e:
        logger.error(f"Error in get_users_previous_messages_history_of_last_30_days: {e}")
        return {"status_code": 500, "data": f"Internal Server Error: {e}"}
    
async def get_server_time():
    try:
        final_time = convert_to_est(time.time(), False)
        print(final_time, "final_time")
        return {"status_code": 200, "data": str(final_time)}
    except Exception as e:
        logger.error(f"Error in get_server_time: {e}")
        return {"status_code": 500, "data": f"Internal Server Error: {e}"}


async def inbound_sms(request):
    try:
        vonage_webhooks_collection = db[constants.VONAGE_WEBHOOKS_COLLECTION]
        request['source'] = 'inbound_sms'
        # convert to EST timezone
        request["created_at"] = convert_to_est(time.time(), False)

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

        # get users previous messages history of last 30 days
        msisdn = request["msisdn"]
        history_response = await get_users_previous_messages_history_of_last_30_days(msisdn)

        if history_response["status_code"] != 200:
            logger.error(f"Error in inbound_sms: {history_response['data']}")
            history_response = {"data": []}

        response = await openai_client.generate_sms_agent_response_with_history(
            context=context, query=query, previous_messages=history_response["data"]
        )
        if response["status_code"] != 200:
            return response
        
        gpt_response = response["response"]
        request['query'] = query  

        if "booking_confirm" in gpt_response:
            response = await train_agent_service.execute_booking_intent(query, history_response["data"], 'SMS')
            gpt_response = response["response"]
        
        elif "event_hiring" in gpt_response:
            response = await train_agent_service.execute_hiring_intent(query, history_response["data"], 'SMS')
            gpt_response = response["response"]
        else:
            event_list = [
                "event_change_orders", "event_new_lead", "event_permit", "event_inspection", "event_collection", "event_dispatching"
            ]
            for event in event_list:
                if event in gpt_response:
                    response = await train_agent_service.execute_intent(query, history_response["data"], event, 'SMS')
                    gpt_response = response["response"]
                    break

        print(gpt_response, "gpt response")

        request["response"] = gpt_response
        vonage_webhooks_collection.insert_one(request)
        
        if channel == "whatsapp":
            logger.info("Sending WhatsApp message")
            response = vonage_api.send_whatsapp_message(to, gpt_response)
        elif channel == "sms":
            logger.info("Sending SMS message")
            response = vonage_api.send_sms(to, gpt_response)

        logger.info("Returning from Inbound SMS service")
        return {"status_code": 200, "data": "Inbound SMS service"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(f"Error in inbound_sms: {e}")
        return {"status_code": 500, "data": f"Internal Server Error: {e}"}


async def sms_status(request):
    try:
        vonage_webhooks_collection = db[constants.VONAGE_WEBHOOKS_COLLECTION]
        request['source'] = 'sms_status'
        request["created_at"] = datetime.now()
        vonage_webhooks_collection.insert_one(request)
        logger.info("Inside SMS Status service")
        return {"status_code": 200, "data": "SMS Status service"}
    except Exception as e:
        logger.error(f"Error in sms_status: {e}")
        return {"status_code": 500, "data": f"Internal Server Error: {e}"}
