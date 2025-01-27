from logging_module import logger
from thirdparty.pinecone_service import PineConeDBService
from config import constants
import blueprints


async def generate_index_service():
    try:
        if constants.DEBUG:
            logger.info("Debug Mode: Skipping Index Creation")
            return
        pinecone = PineConeDBService()
        await pinecone.create_index(constants.PINECONE_INDEX)
        logger.info("Generate Index Service Executed")
    except Exception as e:
        logger.debug(f"Error in Generate Index Service: {e}")


async def generate_embedding_for_text_service(text: str):
    try:
        pinecone = PineConeDBService()
        response = await pinecone._generate_embedding(text)
        logger.info("Embeddings created")
        return response
    except Exception as e:
        logger.debug(f"Error in Generate Embeddings Service: {e}")


async def embed_record_in_db_service(data: blueprints.EmbedRecordsInPineconeDB):
    try:
        pinecone = PineConeDBService()
        response = await pinecone.upsert_data(data.data)
        logger.info("Embeddings created")
        return response
    except Exception as e:
        logger.debug(f"Error in Generate Embeddings Service: {e}")


async def query_records_service(query: str):
    try:
        pinecone = PineConeDBService()
        response = await pinecone.query_data(query)
        if response["status_code"] != 200:
            return response
        matches = response["response"]["matches"]
        formatted_matches = []

        for match in matches:
            formatted_match = {
                "id": match.get("id", ""),
                "metadata": match.get("metadata", ""),
                "score": match.get("score", 0),
                "values": match.get("values", []),
            }
            formatted_matches.append(formatted_match)
        logger.info("Query Completed")
        return {"status_code": 200, "data": formatted_matches}
    except Exception as e:
        logger.debug(f"Error in Query Records Service: {e}")
