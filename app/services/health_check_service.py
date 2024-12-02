from logging_module import logger
from thirdparty.openai_service import OpenAIService
from thirdparty.pinecone_service import PineConeDBService


async def test_openai_service():
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
            "message": "OpenAI service is working correctly.",
            "response": response,
            "status_code": 200,
        }
    except Exception as e:
        logger.error(f"An error occurred while testing the OpenAI service: {e}")
        return {
            "message": f"An error occurred while testing the OpenAI service: {e}",
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
            "message": "PineconeDB service is working correctly.",
            "response": response,
            "status_code": 200,
        }
    except Exception as e:
        logger.error(f"An error occurred while testing the PineconeDB service: {e}")
        return {
            "message": f"An error occurred while testing the PineconeDB service: {e}",
            "status_code": 500,
        }
