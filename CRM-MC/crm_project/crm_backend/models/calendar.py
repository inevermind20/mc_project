from sqlalchemy import Column, Integer, String, DateTime
from db.database import Base

class CalendarEvent(Base):
    __tablename__ = "calendar"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
