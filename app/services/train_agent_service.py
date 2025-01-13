import pdfplumber
from nltk.tokenize import sent_tokenize
import os
from logging_module import logger
from services import PineConeDBService, OpenAIService
from services.client_agent_training_service import get_current_knowledge_books_service
from fastapi import UploadFile, File
import re
import json
import uuid
from models import ServiceTitanBookingRequest, ServiceTitanCustomerContact
from services.service_titan_service import create_booking_request
from services.slack_service import send_block_to_channel
from config import constants
import requests
import re
from datetime import datetime


async def extract_useful_pages(pdf_path, min_words=20, skip_keywords=None):
    try:
        useful_pages = []
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text_simple()
                if not text:
                    continue

                useful_pages.append({"page_number": i + 1, "text": text})
        return {"status_code": 200, "response": useful_pages}
    except Exception as e:
        return {
            "status_code": 500,
            "response": f"Error while extracting useful pages: {e}",
        }
    
def format_receptionist_time(iso_time: str) -> str:
    """
    Convert an ISO 8601 UTC time string to a receptionist-readable format.
    
    Args:
        iso_time (str): The ISO 8601 formatted time string (e.g., 2025-01-12T13:32:00Z).
    Returns:
        str: The formatted time string (e.g., 'Sunday, January 12, 2025 at 1:32 PM').
    """
    try:
        # Parse the ISO 8601 string into a datetime object
        dt = datetime.strptime(iso_time, "%Y-%m-%dT%H:%M:%SZ")
        
        # Format into a receptionist-readable string
        return dt.strftime("%A, %B %d, %Y at %-I:%M %p") 
    except Exception as e:
        logger.error(f"Error formatting time: {e}")
        # extract the date if possible
        return iso_time.split("T")[0]


async def chunk_text(text, max_tokens=900):
    try:
        # sentences = sent_tokenize(text)
        # chunks = []
        # current_chunk = []
        # current_length = 0

        # for sentence in sentences:
        #     sentence_length = len(sentence.split())
        #     if current_length + sentence_length > max_tokens:
        #         chunks.append(" ".join(current_chunk))
        #         current_chunk = []
        #         current_length = 0
        #     current_chunk.append(sentence)
        #     current_length += sentence_length

        # if current_chunk:
        #     chunks.append(" ".join(current_chunk))
        return {"status_code": 200, "response": [text]}
    except Exception as e:
        return {"status_code": 500, "response": f"Error while chunking text: {e}"}


async def store_embeddings_in_pinecone(chunks, knowledge_book_name=None):
    try:
        pinecone_client = PineConeDBService()
        openai_client = OpenAIService()
        cooked_chunks = []
        temp_debug_list = []
        for i, chunk in enumerate(chunks):
            openai_response = await openai_client.generate_text_embeddings(
                chunk["text"]
            )
            temp_debug_list.append(openai_response)
            embedding = openai_response["embedding"]
            metadata = {"page_number": chunk["page_number"], "text": chunk["text"]}
            unique_id = str(uuid.uuid4())
            cooked_chunks.append((f"chunk-{i}-{unique_id}", embedding, metadata))
        pinecone_response = await pinecone_client.populate_cooked_records(cooked_chunks, knowledge_book_name)

        return {
            "status_code": 200,
            "response": len(cooked_chunks),
            "message": pinecone_response["response"],
        }
    except Exception as e:
        return {"status_code": 500, "response": f"Error while storing embeddings: {e}"}


def clean_newlines(text):
    return text


async def upload_pdf_for_training_agent(file: UploadFile = File(...), knowledge_book_name: str = None):    
    # Save uploaded file temporarily
    temp_file_path = f"temp_{file.filename}"
    try:
        
        if knowledge_book_name:
            response = await get_current_knowledge_books_service()
            if response["status_code"] != 200:
                return response
            
            if knowledge_book_name not in response["response"]:
                return {
                    "status_code": 400,
                    "response": f"Knowledge Book '{knowledge_book_name}' does not exist.",
                }


        with open(temp_file_path, "wb") as f:
            f.write(await file.read())

        # Process the PDF
        useful_pages = await extract_useful_pages(temp_file_path)
        if useful_pages["status_code"] != 200:
            return useful_pages

        logger.debug("Useful Pages extracted")
        # Chunk and embed
        all_chunks = []
        for page in useful_pages["response"]:
            page_chunks = await chunk_text(page["text"])
            if page_chunks["status_code"] != 200:
                continue
            for chunk in page_chunks["response"]:
                text_chunk = clean_newlines(chunk)
                all_chunks.append(
                    {"page_number": page["page_number"], "text": text_chunk}
                )
        num_chunks = await store_embeddings_in_pinecone(all_chunks, knowledge_book_name)
        os.remove(temp_file_path)

        if num_chunks["status_code"] != 200:
            return num_chunks

        return {
            "message": f"PDF processed successfully. {num_chunks['response']} chunks stored in Pinecone. {num_chunks['message']}",
            "useful_pages": useful_pages["response"],
            "all_chunks": all_chunks,
            "status_code": 200,
        }
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        return {"status_code": 500, "message": f"Error while training agent: {e}"}

async def detect_booking_intent(user_query: str, previous_messages: list):
    try:
        openai_service = OpenAIService()
        response = await openai_service.get_query_intent(user_query, previous_messages)
        if response["status_code"] != 200:
            return False
        return response["intent"]
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(f"Error detecting booking intent: {e}")
        return False
    
import re

def extract_json(response):
    try:
        match = re.search(r'\{.*\}', response, re.DOTALL)
        if match:
            json_data = match.group()
            return json.loads(json_data)
        else:
            raise ValueError("No valid JSON found in the response")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON: {e}")


async def extract_booking_data(user_query: str, previous_messages: list = None):
    final_response = ""
    try:
        openai_service = OpenAIService()
        response = await openai_service.extract_user_details(user_query, previous_messages)
        if response["status_code"] != 200:
            return response

        details = response["response"].replace("```json", "").replace("```", "").strip()
        final_response = details
        logger.debug(f"Extracted user details: {details}")
        json_data = extract_json(details)
        logger.debug(f"Extracted user details in json format: {json_data}")
        contacts = []
        if "email" in json_data and json_data["email"]:
            contacts.append(ServiceTitanCustomerContact(type="Email", value=json_data["email"]))
        if "phone" in json_data and json_data["phone"]:
            contacts.append(ServiceTitanCustomerContact(type="MobilePhone", value=json_data["phone"]))

        todays_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        return {
            "data": ServiceTitanBookingRequest(
            source="AI Assistant",
            name=json_data.get("name", "Unknown User"),
            summary=user_query,
            isFirstTimeClient=True,
            contacts=contacts,
            start=json_data.get("start", todays_date),
            isSendConfirmationEmail=True,
        ),
            "status_code": 200,
            "raw_data": json_data,
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(f"Error extracting booking data: {e}")
        return {"message": "An error occurred while extracting booking data.", "error": str(e), "status_code": 500, "response": f"Forward this on our contact number: {final_response}"}

async def handle_booking_request(user_query: str, conversation_summary: str = None, previous_messages: list = None):
    try:
        booking_data = await extract_booking_data(user_query, previous_messages)
        if booking_data["status_code"] != 200:
            return booking_data

        json_data = booking_data["raw_data"]
        booking_data = booking_data["data"]
        response = await create_booking_request(booking_data, conversation_summary)
        if response["status_code"] != 200:
            return response
        
        return {"message": "Booking request created successfully", "status_code": 200, "response": response["data"], "booking_data": json_data}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"message": "An error occurred while processing your booking.", "response": str(e), "status_code": 500}


async def query_via_ai_agent(query: str, knowledge_book_name: str = None):
    try:
        pinecone_client = PineConeDBService()
        openai_client = OpenAIService()

        if await detect_booking_intent(query):
            response =  await handle_booking_request(query)
            if response["status_code"] != 200:
                return response
            return {"message": "Booking request created successfully", "status_code": 200, "response": response["response"]}
   
        if knowledge_book_name:
            response = await get_current_knowledge_books_service()
            if response["status_code"] != 200:
                return response
            
            if knowledge_book_name not in response["response"]:
                return {
                    "status_code": 400,
                    "response": f"Knowledge Book '{knowledge_book_name}' does not exist.",
                }
            

        response = await pinecone_client.query_data(query, 3, knowledge_book_name)
        if response["status_code"] != 200:
            return response

        matches = response["response"]["matches"]

        context = " ".join([match["metadata"]["text"] for match in matches])
        response = await openai_client.generate_ai_agent_response(
            context=context, query=query
        )
        if response["status_code"] != 200:
            return response
        return {
            "message": "Agent query processes successfully",
            "query": query,
            "response": response["response"],
            "status_code": 200,
        }
    except Exception as e:
        return {"status_code": 500, "response": f"Error while querying the agent: {e}"}


async def process_tawk_query_service(query: str, knowledge_book_name: str = None):
    try:
        pinecone_client = PineConeDBService()
        openai_client = OpenAIService()

        if await detect_booking_intent(query):
            response =  await handle_booking_request(query)
            if response["status_code"] != 200:
                return response
            return {"message": "Booking request created successfully", "status_code": 200, "response": response["response"]}

        if knowledge_book_name:
            response = await get_current_knowledge_books_service()
            if response["status_code"] != 200:
                return response

            if knowledge_book_name not in response["response"]:
                return {
                    "status_code": 400,
                    "response": f"Knowledge Book '{knowledge_book_name}' does not exist.",
                }

        response = await pinecone_client.query_data(query, 3, knowledge_book_name)
        if response["status_code"] != 200:
            return response

        matches = response["response"]["matches"]

        context = " ".join([match["metadata"]["text"] for match in matches])
        response = await openai_client.generate_ai_agent_response(
            context=context, query=query
        )
        if response["status_code"] != 200:
            return response
        return {
            "response": response["response"],
            "status_code": 200,
        }
    except Exception as e:
        return {"status_code": 500, "response": f"Error while querying the agent: {e}"}


async def get_user_conversation_from_botpress(conversation_id: str):
    try:
        url = f"{constants.BOTPRESS_MESSAGE_ENDPOINT}?conversationId={conversation_id}"

        headers = {
            "accept": "application/json",
            "x-bot-id": constants.BOTPRESS_BOT_ID,
            "authorization": f"Bearer {constants.BOTPRESS_PAT}",
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json_data = response.json()
        print(json_data, "JSON DATA")
        data = convert_to_openai_messages(json_data)
        return {
            "status_code": 200,
            "response": data,
        }
    except Exception as e:
        return {
            "status_code": 500,
            "response": f"Error while getting user conversation: {e}",
        }


def convert_to_openai_messages(data):
    """
    Converts a custom message format to an OpenAI-compatible message list.

    Args:
        data (dict): Input data containing the messages.

    Returns:
        list: List of messages in OpenAI-compatible format.
    """
    try:
        openai_messages = []

        for message in data.get("messages", []):
            role = "assistant" if message.get("direction") == "outgoing" else "user"
            content = message.get("payload", {}).get("text", "")
            if content:  # Only add messages with non-empty content
                openai_messages.append({"role": role, "content": content, "timestamp": message.get("createdAt")})

        return openai_messages
    except Exception as e:
        logger.error(f"Error converting messages: {e}")
        return []


def check_for_malicious_content(query):
    for pattern in constants.dangerous_patterns:
        if re.search(pattern, query, re.IGNORECASE):
            return True
    return None

async def execute_booking_intent(query: str, previous_messages: list):
    try:
        openai_client = OpenAIService()

        conversation_summary = await openai_client.get_conversation_bullets(
                    previous_messages
                )
        summary = conversation_summary["response"]
        response = await handle_booking_request(
            user_query=query,
            conversation_summary=summary,
            previous_messages=previous_messages,
        )
        if response["status_code"] != 200:
            return response

        booking_data = response["booking_data"]

        logger.debug("Sending message to dispatching channel")
        blocks = [
                {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"\nPlease call *{booking_data['name']}* at *{booking_data['phone']}* located at *{booking_data['address']}* to collect *$49 hold* and assign a technician."
                }
                },
                {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Summary:*\n• *Appointment Date:* {format_receptionist_time(booking_data['start'])}\n• *Appointment Details:* {summary}"
                }
                },
                {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f""" *Marketing Source*: Website"""
                }
                }
            ]
        await send_block_to_channel(
            blocks=blocks, channel=constants.SLACK_CHANNEL_DICT["dispatching"]
        )
        logger.debug("Message sent to dispatching channel")
        return {
            "response": f"Awesome. We're working on this now! We will call you shortly to collect a $49 hold (which we'll credit to any work you perform with us) and confirm we have your requested time onto one of our routes. Your booking ID is {response['response']['id']}",
            "status_code": 200,
        }
    except Exception as e:
        return {"status_code": 500, "response": f"Error while executing booking intent: {e}"}
    
"""
permitting, inspections, customer complaints, invoices, estimates/sales questions, change orders, hiring, warranty
"""

async def execute_intent(query: str, previous_messages: list, event_name: str):
    try:
        openai_client = OpenAIService()

        conversation_summary = await openai_client.get_general_conversation_summary(
                    previous_messages
                )
        summary = conversation_summary["response"]

        response = await openai_client.extract_user_basic_details(query, previous_messages)
        if response["status_code"] != 200:
            return response

        details = response["response"].replace("```json", "").replace("```", "").strip()
        print(response, "AI response")
        json_data = json.loads(details)
        logger.debug(f"Extracted user details in json format: {json_data}")
        customer_data = json_data

        logger.debug("Sending message to dispatching channel")
        blocks = [
                {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"""\n Please call *{str(customer_data['name']).title()}* from *{customer_data['address']}* at *{customer_data['phone']}*.
                    """
                }
                },
                {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f""" *Conversation Summary*: {summary}"""
                }
                },
                {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f""" *Marketing Source*: Website"""
                }
                }
            ]

        channel = constants.SLACK_CHANNEL_DICT.get(event_name.replace("event_", ""), None)
        # print(f"Sending message to {event_name.replace('event_', '')} {channel} channel")
        await send_block_to_channel(
            blocks=blocks, channel=channel
        )
        # print(f"Message sent to {event_name.replace("event_", "")} {channel} channel")
        return {
            "response": f"Awesome, we're working on this now! We will call you shortly to discuss your needs.",
            "status_code": 200,
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status_code": 500, "response": f" {e}"}

async def execute_hiring_intent(query: str, previous_messages: list):
    try:
        logger.debug("Inside Hiring Intent")
        openai_client = OpenAIService()

        conversation_summary = await openai_client.get_conversation_summary(
                    previous_messages
                )
        summary = conversation_summary["response"]

        response = await openai_client.extract_user_basic_details(query, previous_messages)
        if response["status_code"] != 200:
            return response

        details = response["response"].replace("```json", "").replace("```", "").strip()

        json_data = json.loads(details)
        logger.debug(f"Extracted user details in json format: {json_data}")
        customer_data = json_data

        logger.debug("Sending message to human resource channel")
        blocks = [
                {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"""\n *{str(customer_data['name']).title()}* at *{customer_data['address']}* was asking about hiring. Please reach out to them at *{customer_data['phone']}*.
                    """
                }
                },
                {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f""" *Conversation Summary*: {summary}"""
                }
                },
                {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f""" *Marketing Source*: Website"""
                }
                }
            ]
        await send_block_to_channel(
            blocks=blocks, channel=constants.SLACK_CHANNEL_DICT["human-resources"]
        )
        logger.debug("Message sent to dispatching channel")
        return {
            "response": f"Awesome, we're working on this now! We will call you shortly to discuss your hiring needs.",
            "status_code": 200,
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status_code": 500, "response": f"Error while executing booking intent: {e}"}


async def process_botpress_query_service(query: str, conversation_id: str):
    logger.debug("Inside Process Botpress Query controller")
    logger.debug(f"Query: {query} Conversation ID: {conversation_id}")
    try:
        if check_for_malicious_content(query):
            return {
                "status_code": 400,
                "response": "Your message contains potentially malicious content. Please striclty use our service for your Electrical needs only.",
            }
        conversation_response = await get_user_conversation_from_botpress(
            conversation_id
        )
        if conversation_response["status_code"] != 200:
            return conversation_response

        previous_messages = conversation_response["response"][::-1]
        print(previous_messages, "Previous Messages")
        pinecone_client = PineConeDBService()
        openai_client = OpenAIService()

        response = await pinecone_client.query_data(query, 3, None)
        if response["status_code"] != 200:
            return response

        matches = response["response"]["matches"]
        context = " ".join([match["metadata"]["text"] for match in matches])

        response = await openai_client.generate_ai_agent_response_with_history(
            context=context, query=query, previous_messages=previous_messages
        )
        if response["status_code"] != 200:
            return response

        print(response["response"])
        
        if "booking_confirm" in response["response"]:
            response = await execute_booking_intent(query, previous_messages)
            return response
        
        if "event_hiring" in response["response"]:
            response = await execute_hiring_intent(query, previous_messages)
            return response
        
        event_list = [
            "event_change_orders", "event_new_lead", "event_permit", "event_inspection", "event_collection", "event_dispatching"
        ]
        for event in event_list:
            if event in response["response"]:
                response = await execute_intent(query, previous_messages, event)
                return response
                

        return {
            "response": response["response"],
            "status_code": 200,
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status_code": 500, "response": f"Error while querying the agent: {e}"}
