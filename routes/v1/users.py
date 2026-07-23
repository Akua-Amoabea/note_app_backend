from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException
from schemas.users import UserSchema
from config.database import get_db
from sqlalchemy.orm import Session
from models.users import PendingUser, User
from core.security import  hash_password
from services.email_services import send_verification_email
from services.otp_services import get_otp_code, save_otp_code


user_router = APIRouter(
    prefix="/v1/users",
    tags=["Users"]
)

@user_router.post("")
async def create_user(user: UserSchema, db: Session = Depends(get_db)):

    email = user.email.strip().lower()

    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        raise HTTPException(
            status_code=409,    
            detail="Email already registered"
        )
    existing_pending_user = db.query(PendingUser).filter(PendingUser.email == email).first()

    if existing_pending_user:
        raise HTTPException(
            status_code=409,    
            detail="Verification Pending. Request for OTP code"
        )
    
    user_password = hash_password(password=user.password)

    db_user = PendingUser(
        first_name=user.first_name,
        last_name=user.last_name,
        email=email,
      password= user_password,
        expires_at= datetime.now()+ timedelta(minutes=30)

    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    otp_code = get_otp_code()

    save_otp_code(email=db_user.email, otp= otp_code)

    send_verification_email(
        email=db_user.email,
        code= otp_code,
        first_name=db_user.first_name

    )

    return {
        "message": "Registered Successfully"
    }

