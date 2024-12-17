from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    role: str
    password: str

    class Config:
        orm_mode = True
