
from services import PineConeDBService, OpenAIService
from logging_module import logger
from fastapi import File





async def create_knowledge_book_service(knowledge_book_name: str):
    try:
        logger.debug("Inside Create Knowledge Book Service")
        response = await get_current_knowledge_books_service()
        if response["status_code"] != 200:
            return response
        
        if knowledge_book_name in response["response"]:
            return {
                "status_code": 400,
                "response": f"Knowledge Book '{knowledge_book_name}' already exists.",
            }
        
        if len(response["response"]) >= 5:
            return {
                "status_code": 400,
                "response": "Maximum number of Knowledge Books reached. Please delete some Knowledge Books to create new ones.",
            }
        knowledge_book_name = knowledge_book_name.lower()

        pinecone = PineConeDBService()
        response = await pinecone.create_new_index(knowledge_book_name)
        logger.info("Knowledge Book created")
        return response
    except Exception as e:
        logger.debug(f"Error in Create Knowledge Book Service: {e}")


async def get_current_knowledge_books_service():
    try:
        pinecone = PineConeDBService()
        response = await pinecone.get_existing_indexes()
        logger.info("Knowledge Books fetched")
        return response
    except Exception as e:
        logger.debug(f"Error in Get Knowledge Books Service: {e}")


async def delete_knowledge_book_service(knowledge_book_name: str):
    try:
        logger.debug("Inside Delete Knowledge Book Service")
        response = await get_current_knowledge_books_service()
        if response["status_code"] != 200:
            return response
        
        if knowledge_book_name not in response["response"]:
            return {
                "status_code": 400,
                "response": f"Knowledge Book '{knowledge_book_name}' does not exist.",
            }
        
        pinecone = PineConeDBService()
        response = await pinecone.delete_index(knowledge_book_name)
        logger.info("Knowledge Book deleted")
        return response
    except Exception as e:
        logger.debug(f"Error in Delete Knowledge Book Service: {e}")


async def update_agent_prompt_service(system_prompt: str):
    try:
        logger.debug("Inside Update Agent Prompt Service")
        openai = OpenAIService()
        response = await openai.update_system_prompt(system_prompt)
        logger.info("Agent Prompt Updated")
        return response
    except Exception as e:
        logger.debug(f"Error in Update Agent Prompt Service: {e}")


async def get_system_prompt_for_ai_agent_service(context: str):
    try:
        logger.debug("Inside Get System Prompt Service")
        openai = OpenAIService()
        response = await openai.get_system_prompt_for_ai_agent(context)
        logger.info("System Prompt fetched")
        return response
    except Exception as e:
        logger.debug(f"Error in Get System Prompt Service: {e}")