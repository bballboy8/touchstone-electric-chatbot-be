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
import pytz


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
            converted_time = message["created_at"]
            est_timezone = pytz.timezone("US/Eastern")
            converted_time = converted_time.astimezone(est_timezone)
            user_content = f"Message Timestamp in EST: {converted_time} \nMessage : {message['query']}"
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


async def get_users_previous_messages_history_of_last_30_days(msisdn, recent_filter=False):
    try:
        created_at = await get_users_recent_conversations_from_db(msisdn)
        vonage_webhooks_collection = db[constants.VONAGE_WEBHOOKS_COLLECTION]
        query = {"msisdn": msisdn, "source": "inbound_sms"}
        print(created_at, recent_filter) 
        if created_at and recent_filter:
            query["created_at"] = {"$gt": created_at}
        else:
            query["created_at"] = {"$gte": datetime.now() - timedelta(days=7)}
        history = await vonage_webhooks_collection.find(query, {'query':1, 'response':1, 'messageId':1, "_id":0, "created_at":1}).to_list(length=None)
        formatted_response = await db_output_formatter_to_openai_format(list(history))
        print(len(formatted_response), "formatted_response", formatted_response)
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


async def get_users_details_in_a_text_chunk_from_db(number):
    try:
        users_collection = db[constants.USERS_COLLECTION]
        number_combinations = [str(number)[1:], str(number)[2:], str(number)]
        query = {
            "$or": [
                {"mobilephone": {"$exists": True, "$elemMatch": {"$in": number_combinations}}},
                {"phone": {"$exists": True, "$elemMatch": {"$in": number_combinations}}},
            ]
        }
        user_details = await users_collection.find_one(query, {"_id": 0,})
        formatted_response = ""
        if not user_details:
            return {"status_code": 200, "data": "Not Available"}
        print(user_details, "user_details")
        for key, value in user_details.items():
            if value and key not in ['service_titan_id', 'tag_id']:
                value = value if isinstance(value, str) else ", ".join(value)
                formatted_response += f"{key}: {value}\n"

        return {"status_code": 200, "data": formatted_response}
    except Exception as e:
        logger.error(f"Error in get_users_details_in_a_text_chunk_from_db: {e}")
        return {"status_code": 500, "data": f"Internal Server Error: {e}"}
    
async def get_users_recent_conversations_from_db(msisdn: str):
    try:
        users_registered_requests_collection = db[constants.USERS_REGISETERED_REQUESTS_COLLECTION]
        response = await users_registered_requests_collection.find({"msisdn": msisdn}).sort("created_at", -1).limit(1).to_list(length=1)
        if response:
            created_at = response[0]["created_at"]
            print("Users last registered request: ", created_at)
            return created_at
    except Exception as e:
        logger.error(f"Error in get_users_recent_conversations_from_db: {e}")
        return None


async def inbound_sms(request):
    try:
        vonage_webhooks_collection = db[constants.VONAGE_WEBHOOKS_COLLECTION]
        users_registered_requests_collection = db[constants.USERS_REGISETERED_REQUESTS_COLLECTION]

        # check if this message request is already registered
        query = {"messageId": request["messageId"]}
        if await vonage_webhooks_collection.find_one(query) and not constants.DEBUG:
            logger.info("Message Request already registered")
            return {"status_code": 200, "data": "Message already registered"}


        request['source'] = 'inbound_sms'
        # convert to EST timezone
        request["created_at"] = convert_to_est(time.time(), False)

        print("created at time", request["created_at"])
        vonage_api = VonageApi()
        openai_client = OpenAIService()
        pinecone_client = PineConeDBService()

        query = request["text"]

        channel = "sms"
        if "channel" in request:
            channel = request["channel"]

        to = request["msisdn"]

        

        user_details = await get_users_details_in_a_text_chunk_from_db(to)
        if user_details["status_code"] != 200:
            logger.error(f"Error in inbound_sms: {user_details['data']}")
            user_details = {"data": "Not Available"}

        response = await pinecone_client.query_data(query, 2, None)
        if response["status_code"] != 200:
            print(response)
            logger.error(f"Error in pinecone inbound_sms: {response['response']}")
            response = {"response": {"matches": []}}

        matches = response["response"]["matches"]
        # get the ids of the matches
        matches_ids = [match["id"] for match in matches]
        print(matches_ids, "matches_ids")
        context = " ".join([match["metadata"]["text"] for match in matches])

        # get users previous messages history of last 30 days
        msisdn = request["msisdn"]
        history_response = await get_users_previous_messages_history_of_last_30_days(msisdn, True)

        if history_response["status_code"] != 200:
            logger.error(f"Error in inbound_sms: {history_response['data']}")
            history_response = {"data": []}

        print(len(history_response["data"]), "history_response")

        response = await openai_client.generate_sms_agent_response_with_history(
            context=context, query=query, previous_messages=history_response["data"], user_details=user_details["data"]
        )
        if response["status_code"] != 200:
            return response
        
        gpt_response = response["response"]
        request['query'] = query

        print("Initial GPT Response: ", gpt_response)  

        has_event = False
        data = {
            "msisdn": to,
        }
        if "booking_confirm" in gpt_response:
            response = await train_agent_service.execute_booking_intent(query, history_response["data"], 'SMS')
            data["event"] = "booking_confirm"
            has_event = True
        
        elif "event_hiring" in gpt_response:
            response = await train_agent_service.execute_hiring_intent(query, history_response["data"], 'SMS')
            data["event"] = "event_hiring"
            has_event = True
        else:
            event_list = [
                "event_change_orders", "event_new_lead", "event_permit", "event_inspection", "event_collection", "event_dispatching"
            ]
            for event in event_list:
                if event in gpt_response:
                    response = await train_agent_service.execute_intent(query, history_response["data"], event, 'SMS')
                    data["event"] = event
                    has_event = True
                    break
        
        if has_event:
            gpt_response = response["response"]
            data["created_at"] = request["created_at"]
            users_registered_requests_collection.insert_one(data)
        
        print("Final GPT Response : ", gpt_response)

        request["response"] = gpt_response
        vonage_webhooks_collection.insert_one(request)
        
        if channel == "sms":
            logger.info("Sending SMS message")
            if constants.DEBUG:return
            response = vonage_api.send_sms(to, request["response"])

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
