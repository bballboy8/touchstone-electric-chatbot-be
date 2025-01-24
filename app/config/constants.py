import os
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

load_dotenv()

# Environment
DEBUG = os.getenv("DEBUG", "False") == "True"

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
# BOTPRESS_BOT_ID="fc6f4bb1-681e-4a0f-a358-26459df0db09"
# BOTPRESS_PAT="bp_pat_0OJIp1WPAK2jKoI3sHwB65teRCEQsqkU2B8N"
BOTPRESS_BOT_ID="9a8082a3-f096-4dff-abf4-6d13752ac256"
BOTPRESS_PAT="bp_pat_0MOHLwpIru69iZwU6N85xl6T9GQqGNwnWw3Y"

# Vonage
VONAGE_FROM_NUMBER = os.getenv("VONAGE_FROM_NUMBER")
VONAGE_API_KEY = os.getenv("VONAGE_API_KEY")
VONAGE_API_SECRET = os.getenv("VONAGE_API_SECRET")
VONAGE_APPLICATION_ID = os.getenv("VONAGE_APPLICATION_ID")


BOOKING_INTENT_CONSTANTS = ["BOOK", "APPOINTMENT", "SCHEDULE", "RESERVE"]


dangerous_patterns = [
    r"(\{|\}|\[|\]|\<|\>|\;|\!|\&|\$|\=|\$)",  # Common dangerous characters like braces, semicolons, etc.
    r"(exec|eval|import|os\.system|__import__)",  # Malicious Python commands
    r"ignore[ \t]*previous[ \t]*instructions",  # Attempts to change the model's behavior
    r"drop\s+database",  # Example of SQL injection attempts
    r"alert\(",  # Common for JavaScript injection attempts
    r"document\.location",  # Common JavaScript-based attacks
]

# Slack Channel Dictionary
SLACK_CHANNEL_DICT = {
    "dispatching": "C070C3FEQJ1", #done
    "permit": "C073V2Q500M", #done
    "inspection": "C073V2Q500M", #done
    "human-resources": "C07V5BTT8UC", #done
    "collection": "C07QLFVK6D6", #done
    "change_orders": "C08381PAWP3", #done
    "dev-team": "C080R3ALW3V",
    "customer-ai-agent-testing": "C083RC1MB09"
}

# Notion
NOTION_API_TOKEN=os.getenv("NOTION_API_TOKEN")
NOTION_TEAM_CONTACT_PAGE_DATABASE_ID=os.getenv("NOTION_TEAM_CONTACT_PAGE_DATABASE_ID")


# Mongodb Collections

USERS_COLLECTION = "users"
VONAGE_WEBHOOKS_COLLECTION = "vonage_webhooks" if not DEBUG else "vonage_webhooks_local"