from pydantic import BaseModel

class ClientBase(BaseModel):
    name: str
    email: str
    phone: str
    company: str

class ClientCreate(ClientBase):
    pass

class ClientOut(ClientBase):
    id: int

    class Config:
        orm_mode = True
