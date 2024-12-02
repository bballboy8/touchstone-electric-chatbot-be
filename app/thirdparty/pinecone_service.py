from config import constants
from logging_module import logger
from pinecone.grpc import PineconeGRPC as Pinecone



class PineConeDBService:
    def __init__(self):
        """
        Initialize the Pinecone service with the API key from the constants file.
        """
        self.pinecone_client = Pinecone(
            api_key=constants.PINECONEDB_API_KEY,
        )

    async def test_connection(self):
        """
        Test the Pinecone DB connection by listing indexes or checking API reachability.
        Returns:
            bool: True if connection is successful, False otherwise.
        """
        try:
            response = self.pinecone_client.list_indexes()
            logger.info("Pinecone DB connection successful")
            return {"status_code": 200, "response": list(response)}
        except Exception as e:
            logger.error("Failed to connect to Pinecone DB: %s", e)
            return {"status_code": 500, "response": f"{e}"}
