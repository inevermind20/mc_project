from pydantic import BaseModel

class ProposalBase(BaseModel):
    title: str
    description: str
    client_id: int

class ProposalCreate(ProposalBase):
    pass

class ProposalOut(ProposalBase):
    id: int

    class Config:
        orm_mode = True
