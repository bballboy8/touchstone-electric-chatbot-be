from fastapi import APIRouter
import services
import schemas
from logging_module import logger
import blueprints

router = APIRouter()


@router.get(
    "/generate-embedding",
)
async def generate_embedding_using_pinecone(query: str):
    logger.debug("Inside Generate Embedding using pinecone controller")
    response = await services.generate_embedding_for_text_service(query)
    logger.debug("Response from Generate Embedding using pinecone service")
    return response


@router.post(
    "/embed-records-in-db",
)
async def embed_record_in_db(data: blueprints.EmbedRecordsInPineconeDB):
    logger.debug("Inside Embed records in Pinecone controller")
    response = await services.embed_record_in_db_service(data)
    logger.debug("Response from Embed records in Pinecone service")
    return response


@router.get("/query-records")
async def query_records(query: str):
    logger.debug("Inside Query records in Pinecone controller")
    response = await services.query_records_service(query)
    logger.debug("Response from Query records in Pinecone service")
    return response
