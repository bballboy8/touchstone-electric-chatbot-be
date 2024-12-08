import os
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

load_dotenv()


ALGORITHM = "HS256"
SECRET_KEY = "secret"
DEFAULT_TOKEN_EXPIRY_HOURS = 3600
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/token")


LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")


user = {
    "email": "backend@mailinator.com",
    "password": "Test@123",
    "full_name": "Backend User",
    "_id": "60f3b3b3b3b3b3b3b3b3b3b3",
}

# Environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONEDB_API_KEY = os.getenv("PINECONEDB_API_KEY")


# Index
PINECONE_INDEX = "ai-agent-index"
EMBEDDING_MODEL = "text-embedding-3-small"
