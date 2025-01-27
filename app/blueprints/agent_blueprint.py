from pydantic import BaseModel

class BotPressRequest(BaseModel):
    message: str
    conversation_id: str
    api_key: str