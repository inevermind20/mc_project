from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from models.assistance import Assistance
from schemas.assistance import AssistanceCreate, AssistanceOut

router = APIRouter()

@router.post("/", response_model=AssistanceOut)
def create_assistance(assistance: AssistanceCreate, db: Session = Depends(get_db)):
    db_assistance = Assistance(**assistance.dict())
    db.add(db_assistance)
    db.commit()
    db.refresh(db_assistance)
    return db_assistance

@router.get("/", response_model=list[AssistanceOut])
def list_assistances(db: Session = Depends(get_db)):
    return db.query(Assistance).all()
