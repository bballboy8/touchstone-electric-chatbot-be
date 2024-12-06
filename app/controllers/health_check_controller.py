from fastapi import APIRouter
import services
from logging_module import logger

router = APIRouter()


@router.get(
    "/openai-chat-completion",
)
async def openai_health_chat_completion_check():
    logger.debug("Inside OpenAI health check chat completion controller")
    response = await services.test_openai_chat_completion_service()
    logger.debug("Response from OpenAI health check chat completion  controller")
    return response

@router.get(
    "/openai-text-embeddings",
)
async def openai_health_text_embeddings_check():
    logger.debug("Inside OpenAI health check Text Embeddings controller")
    response = await services.test_openai_for_text_embeddings_service()
    logger.debug("Response from OpenAI health check Text Embeddings controller")
    return response

@router.get(
    "/pineconedb",
)
async def pinecone_health_check():
    logger.debug("Inside pinecone health check controller")
    response = await services.test_pinconedb_service()
    logger.debug("Response from pinecone health check controller")
    return response

