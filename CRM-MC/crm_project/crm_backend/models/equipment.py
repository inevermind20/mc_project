from sqlalchemy import Column, Integer, String, ForeignKey
from db.database import Base

class Equipment(Base):
    __tablename__ = "equipments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    serial_number = Column(String, unique=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
