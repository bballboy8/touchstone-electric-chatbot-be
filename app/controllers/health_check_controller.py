from fastapi import APIRouter, Depends
import services
from logging_module import logger
from utils.dependencies import get_current_user_id
from fastapi.responses import JSONResponse
router = APIRouter()


@router.get(
    "/openai-chat-completion",
)
async def openai_health_chat_completion_check(user_id: int = Depends(get_current_user_id)):
    logger.debug("Inside OpenAI health check chat completion controller")
    response = await services.test_openai_chat_completion_service()
    logger.debug("Response from OpenAI health check chat completion  controller")
    return response

@router.get(
    "/openai-text-embeddings",
)
async def openai_health_text_embeddings_check(user_id: int = Depends(get_current_user_id)):
    logger.debug("Inside OpenAI health check Text Embeddings controller")
    response = await services.test_openai_for_text_embeddings_service()
    logger.debug("Response from OpenAI health check Text Embeddings controller")
    return response

@router.get(
    "/pineconedb",
)
async def pinecone_health_check(user_id: int = Depends(get_current_user_id)):
    logger.debug("Inside pinecone health check controller")
    response = await services.test_pinconedb_service()
    logger.debug("Response from pinecone health check controller")
    return response

@router.get(
    "/service-titan-api",
)
async def service_titan_api_health_check(user_id: int = Depends(get_current_user_id)):
    logger.debug("Inside Service Titan API health check controller")
    response = await services.test_service_titan_api_service()
    logger.debug("Response from Service Titan API health check controller")
    return response

@router.get(
    "/database",
)
async def database_health_check(user_id: int = Depends(get_current_user_id)):
    logger.debug("Inside Database health check controller")
    response = await services.test_database_service()
    logger.debug("Response from Database health check controller")
    return JSONResponse(content=response, status_code=response["status_code"])

@router.get(
    "/notion-api",
)
async def notion_api_health_check(user_id: int = Depends(get_current_user_id)):
    logger.debug("Inside Notion API health check controller")
    response = await services.notion_health_check_service()
    logger.debug("Response from Notion API health check controller")
    return JSONResponse(content=response, status_code=response["status_code"])

@router.get(
    "/gmail-api",
)
async def gmail_api_health_check(user_id: int = Depends(get_current_user_id)):
    logger.debug("Inside Gmail API health check controller")
    response = await services.gmail_health_check_service()
    logger.debug("Response from Gmail API health check controller")
    return JSONResponse(content=response, status_code=response["status_code"])

@router.get(
    "/all-services",
)
async def all_services_health_check(user_id: int = Depends(get_current_user_id)):
    logger.debug("Inside All Services health check controller")
    response = await services.test_all_services()
    logger.debug("Response from All Services health check controller")
    return response