from logging_module import logger
from thirdparty.openai_service import OpenAIService
from thirdparty.pinecone_service import PineConeDBService
from thirdparty.service_titan_api_service import ServiceTitanApiService
from thirdparty.notion_api_service import NotionApiClient
from thirdparty.gmail_service import GmailAPIService
from db_connection import db

async def test_openai_chat_completion_service():
    """
    Test the OpenAI service by sending a sample prompt.

    Returns:
        Object: A message indicating whether the service is working correctly.
    """
    try:
        openai_service = OpenAIService()
        response = await openai_service.test_openai_for_chat_completion()
        if response["status_code"] != 200:
            return response
        return {
            "response": "OpenAI service is working correctly.",
            "status_code": 200,
        }
    except Exception as e:
        logger.error(f"An error occurred while testing the OpenAI service: {e}")
        return {
            "message": f"An error occurred while testing the OpenAI service: {e}",
            "status_code": 500,
        }
    
async def test_openai_for_text_embeddings_service():
    """
    Test the OpenAI service by sending a sample prompt.

    Returns:
        Object: A message indicating whether the service is working correctly.
    """
    try:
        openai_service = OpenAIService()
        response = await openai_service.generate_text_embeddings("apple")
        if response["status_code"] != 200:
            return response
        return {
            "response": "OpenAI service is working correctly for generating embeddings.",
            "status_code": 200,
        }
    except Exception as e:
        logger.error(f"An error occurred while testing the OpenAI service: {e}")
        return {
            "response": f"An error occurred while testing the OpenAI service: {e}",
            "status_code": 500,
        }


async def test_pinconedb_service():
    """
    Test the PineConeDB service by checking the list of index.

    Returns:
    """
    try:
        pinecone_client = PineConeDBService()
        response = await pinecone_client.test_connection()
        if response["status_code"] != 200:
            return response
        return {
            "response": "PineconeDB service is working correctly.",
            "status_code": 200,
        }
    except Exception as e:
        logger.error(f"An error occurred while testing the PineconeDB service: {e}")
        return {
            "response": f"An error occurred while testing the PineconeDB service: {e}",
            "status_code": 500,
        }

async def test_service_titan_api_service():
    """
    Test the Service Titan API service by checking the list of employees.

    Returns:
    """
    try:
        service_titan_api_service = ServiceTitanApiService()
        response = await service_titan_api_service.health_check()
        if response["status_code"] != 200:
            return response
        return {

            "response": "Service Titan API service is working correctly.",
            "status_code": 200,
        }
    except Exception as e:
        logger.error(f"An error occurred while testing the Service Titan API service: {e}")
        return {
            "response": f"An error occurred while testing the Service Titan API service: {e}",
            "status_code": 500,
        }
    
async def test_database_service():
    """
    Test the database service by checking the list of collections.

    Returns:
    """
    try:
        await db.list_collection_names()
        return {"response": "Database Connection Successful", "status_code": 200}
    except Exception as e:
        return {"response": "Internal Server Error", "status_code": 500}
    

async def notion_health_check_service():
    """
    Test the Notion API service by checking the list of team contacts.

    Returns:
    """
    try:
        notion_client = NotionApiClient()
        response = await notion_client.notion_health_check()
        if response["status_code"] != 200:
            return response
        return {
            "response": "Notion API service is working correctly.",
            "status_code": 200,
        }
    except Exception as e:
        logger.error(f"An error occurred while testing the Notion API service: {e}")
        return {
            "response": f"An error occurred while testing the Notion API service: {e}",
            "status_code": 500,
        }
    
async def gmail_health_check_service():
    """
    Test the Gmail API service by checking the user profile.

    Returns:
    """
    try:
        gmail_service = GmailAPIService()
        response = await gmail_service.gmail_health_check()
        if response["status_code"] != 200:
            return response
        return {
            "response": "Gmail API service is working correctly.",
            "status_code": 200,
        }
    except Exception as e:
        logger.error(f"An error occurred while testing the Gmail API service: {e}")
        return {
            "response": f"An error occurred while testing the Gmail API service: {e}",
            "status_code": 500,
        }
    
async def test_all_services():
    """
    Test all the services.

    Returns:
    """
    try:
        response = {
            "openai_chat_completion": await test_openai_chat_completion_service(),
            "openai_text_embeddings": await test_openai_for_text_embeddings_service(),
            "pineconedb": await test_pinconedb_service(),
            "service_titan_api": await test_service_titan_api_service(),
            "database": await test_database_service(),
            "notion_api": await notion_health_check_service(),
            "gmail_api": await gmail_health_check_service(),
        }
        return response
    except Exception as e:
        logger.error(f"An error occurred while testing all services: {e}")
        return {
            "response": f"An error occurred while testing all services: {e}",
            "status_code": 500,
        }