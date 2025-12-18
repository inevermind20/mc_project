from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from db.database import Base

class Assistance(Base):
    __tablename__ = "assistances"
    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipments.id"))
    technician = Column(String)
    description = Column(String)
    date = Column(DateTime)
