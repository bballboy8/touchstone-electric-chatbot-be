from pydantic import BaseModel
from pydantic import EmailStr

class User(BaseModel):
    full_name: str
    email: EmailStr
    password: str
