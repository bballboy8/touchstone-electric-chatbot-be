from config import constants
from logging_module import logger
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import uuid
from thirdparty.openai_service import OpenAIService


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
            return {"status_code": 200, "response": "Pinecone working properly"}
        except Exception as e:
            logger.error(f"Failed to connect to Pinecone DB: {e}")
            return {"status_code": 500, "response": f"{e}"}

    async def create_index(self, index_name, dimension=1536, metric="cosine"):
        """
        Create a Pinecone index if it does not exist.
        Args:
            index_name (str): The name of the index.
            dimension (int): The dimensionality of the vectors.
            metric (str): Similarity metric (e.g., cosine, euclidean).
        Returns:
            dict: Response with status code and message.
        """
        try:
            existing_index = [
                index["name"] for index in self.pinecone_client.list_indexes()
            ]
            if index_name not in existing_index:
                self.pinecone_client.create_index(
                    index_name,
                    dimension=dimension,
                    metric=metric,
                    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
                )
                logger.info(f"Index {index_name} created successfully.")
                return {
                    "status_code": 200,
                    "response": f"Index '{index_name}' created.",
                }
            else:
                logger.info(
                    f"Index {index_name} already exists.",
                )
                return {
                    "status_code": 200,
                    "response": f"Index '{index_name}' already exists.",
                }
        except Exception as e:
            logger.error(f"Failed to create index {index_name}: {e}")
            return {"status_code": 500, "response": str(e)}

    async def upsert_data(self, data):
        """
        Embed and upsert data into the specified Pinecone index.
        Args:
            data (list[dict]): A list of dictionaries containing the records.
        Returns:
            dict: Response with status code and message.
        """
        try:
            index = self.pinecone_client.Index(constants.PINECONE_INDEX)

            upsert_list = []
            for record in data:
                if not isinstance(record, dict):
                    logger.warning(f"Skipping invalid record: {record}")
                    continue
                record_id = str(uuid.uuid4())
                record_text = " ".join(
                    f"{value}" for _, value in record.items() if value
                )
                embedding = await self._generate_embedding(record_text)

                if embedding["status_code"] != 200:
                    return embedding
                embedding_value = embedding["response"]
                upsert_list.append(
                    {"id": record_id, "values": embedding_value, "metadata": record}
                )

            if upsert_list:
                index.upsert(upsert_list)
                return {
                    "status_code": 200,
                    "response": f"{len(upsert_list)} records upserted.",
                }
            else:
                logger.warning("No valid records to upsert.")
                return {"status_code": 400, "response": "No valid records to upsert."}
        except Exception as e:
            logger.error(
                f"Failed to upsert data into index {constants.PINECONE_INDEX}: {e}"
            )
            return {"status_code": 500, "response": str(e)}

    async def query_data(self, query_text, top_k=3):
        """
        Query the specified Pinecone index using a text query.
        Args:
            query_text (str): The query text.
            top_k (int): Number of top results to retrieve.
        Returns:
            dict: Response with status code and query results.
        """
        try:
            index = self.pinecone_client.Index(constants.PINECONE_INDEX)
            query_embedding = await self._generate_embedding(query_text)
            if query_embedding["status_code"] != 200:
                return query_embedding
            query_embedding = query_embedding["response"]
            results = index.query(
                vector=query_embedding, top_k=top_k, include_metadata=True
            )

            if results.get("matches"):
                return {"status_code": 200, "response": results}

            return {"status_code": 404, "response": "No matching records found."}
        except Exception as e:
            logger.error(f"Failed to query index {constants.PINECONE_INDEX}: {e}")
            return {"status_code": 500, "response": str(e)}

    async def _generate_embedding(self, text):
        """
        Generate an embedding for the given text using OpenAI's Embedding API.
        Args:
            text (str): The text to embed.
            engine (str): The embedding model to use.
        Returns:
            list: The embedding vector.
        """
        try:
            openai_client = OpenAIService()
            response = await openai_client.generate_text_embeddings(text)
            if response["status_code"] != 200:
                return response
            embeddings = response["embedding"]
            return {"status_code": 200, "response": embeddings}
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            return {"status_code": 500, "response": str(e)}

    async def populate_cooked_records(self, cooked_record):
        try:
            index = self.pinecone_client.Index(constants.PINECONE_INDEX)
            index.upsert(cooked_record)
            return {
                "status_code": 200,
                "response": "Record upserted",
            }
        except Exception as e:
            logger.error(f"Failed to Populate Cooked Record: {e}")
            return {"status_code": 500, "response": str(e)}
