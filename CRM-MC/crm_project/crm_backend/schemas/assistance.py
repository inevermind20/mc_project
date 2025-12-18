from pydantic import BaseModel
from datetime import datetime

class AssistanceBase(BaseModel):
    equipment_id: int
    technician: str
    description: str
    date: datetime

class AssistanceCreate(AssistanceBase):
    pass

class AssistanceOut(AssistanceBase):
    id: int

    class Config:
        orm_mode = True
