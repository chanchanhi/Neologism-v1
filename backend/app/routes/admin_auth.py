from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import AdminUser
from app.utils import verify_password
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/admin/login")
def login_admin(request: LoginRequest, db: Session = Depends(get_db)):
    admin = db.query(AdminUser).filter(AdminUser.username == request.username).first()
    if not admin or not verify_password(request.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="인증 실패")
    return {"token": "admintoken"}

