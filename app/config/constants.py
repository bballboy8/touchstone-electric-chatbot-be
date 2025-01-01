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
BOTPRESS_MESSAGE_ENDPOINT="https://api.botpress.cloud/v1/chat/messages"
BOTPRESS_BOT_ID="fc6f4bb1-681e-4a0f-a358-26459df0db09"
BOTPRESS_PAT="bp_pat_0OJIp1WPAK2jKoI3sHwB65teRCEQsqkU2B8N"


BOOKING_INTENT_CONSTANTS = ["BOOK", "APPOINTMENT", "SCHEDULE", "RESERVE"]


dangerous_patterns = [
    r"(\{|\}|\[|\]|\<|\>|\;|\!|\&|\$|\=|\$)",  # Common dangerous characters like braces, semicolons, etc.
    r"(exec|eval|import|os\.system|__import__)",  # Malicious Python commands
    r"ignore[ \t]*previous[ \t]*instructions",  # Attempts to change the model's behavior
    r"drop\s+database",  # Example of SQL injection attempts
    r"alert\(",  # Common for JavaScript injection attempts
    r"document\.location",  # Common JavaScript-based attacks
]