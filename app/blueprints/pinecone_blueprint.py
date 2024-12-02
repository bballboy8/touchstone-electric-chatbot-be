from typing import List
from pydantic import BaseModel

class EmbedRecordsInPineconeDB(BaseModel):
    data: List[dict]
