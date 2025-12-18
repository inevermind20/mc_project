from sqlalchemy import Column, Integer, String, ForeignKey
from db.database import Base

class Proposal(Base):
    __tablename__ = "proposals"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    client_id = Column(Integer, ForeignKey("clients.id"))
