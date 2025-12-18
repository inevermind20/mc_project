from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.client import Client
from schemas.client import ClientCreate, ClientOut

router = APIRouter()

@router.post("/", response_model=ClientOut)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    db_client = Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@router.get("/", response_model=list[ClientOut])
def list_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()

from auth.dependencies import require_role

@router.delete("/{id}")
def delete_client(id: int, user = Depends(require_role("admin"))):
    # Só admins podem apagar clientes
    ...

# Podes também permitir múltiplos papéis:
def require_roles(roles: list[str]):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Acesso negado")
        return user
    return role_checker
