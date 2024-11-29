from logging_module import logger
from thirdparty.openai_service import OpenAIService


async def test_openai_service() -> str:
    """
    Test the OpenAI service by sending a sample prompt.

    Returns:
        str: A message indicating whether the service is working correctly.
    """
    try:
        openai_service = OpenAIService()
        response = await openai_service.test_openai_for_chat_completion()
        if response["status_code"] != 200:
            return response
        return {"message": "OpenAI service is working correctly.", "response": response}
    except Exception as e:
        logger.error(f"An error occurred while testing the OpenAI service: {e}")
        return {"message": f"An error occurred while testing the OpenAI service: {e}"}
