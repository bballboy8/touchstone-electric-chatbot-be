import os
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Environment
DEBUG = os.getenv("DEBUG", "False") == "True"
print(f"DEBUG: {DEBUG}")

ALGORITHM = "HS256"
SECRET_KEY = "secret"  # Consider replacing this with os.getenv("SECRET_KEY") for security
DEFAULT_TOKEN_EXPIRY_HOURS = 3600
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/token")

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
print(f"LOG_LEVEL: {LOG_LEVEL}")

user = {
    "email": "a.khan@touchstoneelectric.com",
    "password": "P3@£'a60o5",  # Consider moving this to environment variables
    "full_name": "Backend User",
    "_id": "60f3b3b3b3b3b3b3b3b3b3b3",
}

# Environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(f"OPENAI_API_KEY: {OPENAI_API_KEY}")

PINECONEDB_API_KEY = os.getenv("PINECONEDB_API_KEY")
print(f"PINECONEDB_API_KEY: {PINECONEDB_API_KEY}")

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

print(f"SERVICE_TITAN_TENANT_ID: {SERVICE_TITAN_TENANT_ID}")
print(f"SERVICE_TITAN_CLIENT_ID: {SERVICE_TITAN_CLIENT_ID}")
print(f"SERVICE_TITAN_CLIENT_SECRET: {SERVICE_TITAN_CLIENT_SECRET}")
print(f"SERVICE_TITAN_BASE_AUTH_URL: {SERVICE_TITAN_BASE_AUTH_URL}")
print(f"SERVICE_TITAN_BASE_API_URL: {SERVICE_TITAN_BASE_API_URL}")
print(f"SERVICE_TITAN_APP_KEY: {SERVICE_TITAN_APP_KEY}")
print(f"SERVICE_TITAN_BOOKING_PROVIDER_ID: {SERVICE_TITAN_BOOKING_PROVIDER_ID}")

# Slack
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
print(f"SLACK_BOT_TOKEN: {SLACK_BOT_TOKEN}")
print(f"SLACK_SIGNING_SECRET: {SLACK_SIGNING_SECRET}")

BOTPRESS_MESSAGE_ENDPOINT = "https://api.botpress.cloud/v1/chat/messages"
BOTPRESS_BOT_ID = "9a8082a3-f096-4dff-abf4-6d13752ac256"
BOTPRESS_PAT = "bp_pat_0MOHLwpIru69iZwU6N85xl6T9GQqGNwnWw3Y"

# Vonage
VONAGE_FROM_NUMBER = os.getenv("VONAGE_FROM_NUMBER")
VONAGE_API_KEY = os.getenv("VONAGE_API_KEY")
VONAGE_API_SECRET = os.getenv("VONAGE_API_SECRET")
VONAGE_APPLICATION_ID = os.getenv("VONAGE_APPLICATION_ID")

print(f"VONAGE_FROM_NUMBER: {VONAGE_FROM_NUMBER}")
print(f"VONAGE_API_KEY: {VONAGE_API_KEY}")
print(f"VONAGE_API_SECRET: {VONAGE_API_SECRET}")
print(f"VONAGE_APPLICATION_ID: {VONAGE_APPLICATION_ID}")

# Notion
NOTION_API_TOKEN = os.getenv("NOTION_API_TOKEN")
NOTION_TEAM_CONTACT_PAGE_DATABASE_ID = os.getenv("NOTION_TEAM_CONTACT_PAGE_DATABASE_ID")

print(f"NOTION_API_TOKEN: {NOTION_API_TOKEN}")
print(f"NOTION_TEAM_CONTACT_PAGE_DATABASE_ID: {NOTION_TEAM_CONTACT_PAGE_DATABASE_ID}")

# MongoDB Collections
USERS_COLLECTION = "users"
VONAGE_WEBHOOKS_COLLECTION = "vonage_webhooks"
USERS_REGISETERED_REQUESTS_COLLECTION = "users_registered_requests"
USERS_MESSAGE_TRIGGER_REQUESTS_COLLECTION = "users_message_trigger_requests"
USERS_CAMPAIGN_MESSAGES_COLLECTION = "users_campaign_messages"

# Print MongoDB collection names for debugging
print(f"MongoDB Collections: {USERS_COLLECTION}, {VONAGE_WEBHOOKS_COLLECTION}, {USERS_REGISETERED_REQUESTS_COLLECTION}, {USERS_MESSAGE_TRIGGER_REQUESTS_COLLECTION}, {USERS_CAMPAIGN_MESSAGES_COLLECTION}")


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