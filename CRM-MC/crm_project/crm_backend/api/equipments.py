from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from models.equipment import Equipment
from schemas.equipment import EquipmentCreate, EquipmentOut

router = APIRouter()

@router.post("/", response_model=EquipmentOut)
def create_equipment(equipment: EquipmentCreate, db: Session = Depends(get_db)):
    db_equipment = Equipment(**equipment.dict())
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return db_equipment

@router.get("/", response_model=list[EquipmentOut])
def list_equipments(db: Session = Depends(get_db)):
    return db.query(Equipment).all()
