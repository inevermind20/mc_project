from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from models.proposal import Proposal
from schemas.proposal import ProposalCreate, ProposalOut

router = APIRouter()

@router.post("/", response_model=ProposalOut)
def create_proposal(proposal: ProposalCreate, db: Session = Depends(get_db)):
    db_proposal = Proposal(**proposal.dict())
    db.add(db_proposal)
    db.commit()
    db.refresh(db_proposal)
    return db_proposal

@router.get("/", response_model=list[ProposalOut])
def list_proposals(db: Session = Depends(get_db)):
    return db.query(Proposal).all()
