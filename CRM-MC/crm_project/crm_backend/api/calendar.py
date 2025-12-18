from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from models.calendar import CalendarEvent
from schemas.calendar import CalendarEventCreate, CalendarEventOut

router = APIRouter()

@router.post("/", response_model=CalendarEventOut)
def create_event(event: CalendarEventCreate, db: Session = Depends(get_db)):
    db_event = CalendarEvent(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.get("/", response_model=list[CalendarEventOut])
def list_events(db: Session = Depends(get_db)):
    return db.query(CalendarEvent).all()
