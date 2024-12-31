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
PINECONE_INDEX = "knowledge-book-7"
EMBEDDING_MODEL = "text-embedding-3-small"

SERVICE_TITAN_TENANT_ID = os.getenv("SERVICE_TITAN_TENANT_ID")
SERVICE_TITAN_CLIENT_ID = os.getenv("SERVICE_TITAN_CLIENT_ID")
SERVICE_TITAN_CLIENT_SECRET = os.getenv("SERVICE_TITAN_CLIENT_SECRET")
SERVICE_TITAN_BASE_AUTH_URL = os.getenv("SERVICE_TITAN_BASE_AUTH_URL")
SERVICE_TITAN_BASE_API_URL = os.getenv("SERVICE_TITAN_BASE_API_URL")
SERVICE_TITAN_APP_KEY = os.getenv("SERVICE_TITAN_APP_KEY")
SERVICE_TITAN_BOOKING_PROVIDER_ID = os.getenv("SERVICE_TITAN_BOOKING_PROVIDER_ID")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
BOTPRESS_MESSAGE_ENDPOINT=os.getenv("BOTPRESS_MESSAGE_ENDPOINT")
BOTPRESS_BOT_ID=os.getenv("BOTPRESS_BOT_ID")
BOTPRESS_PAT=os.getenv("BOTPRESS_PAT")


BOOKING_INTENT_CONSTANTS = ["BOOK", "APPOINTMENT", "SCHEDULE", "RESERVE"]