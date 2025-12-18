from pydantic import BaseModel

class EquipmentBase(BaseModel):
    name: str
    serial_number: str
    client_id: int

class EquipmentCreate(EquipmentBase):
    pass

class EquipmentOut(EquipmentBase):
    id: int

    class Config:
        orm_mode = True
