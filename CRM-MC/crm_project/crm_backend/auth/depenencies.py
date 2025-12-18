# função de verificação de permissões
from fastapi import Depends, HTTPException
from models.user import User

def get_current_user():
    # Aqui deves implementar a lógica para extrair o utilizador do token JWT
    ...

def require_role(role: str):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Acesso negado")
        return user
    return role_checker
