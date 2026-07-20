
from fastapi import APIRouter, HTTPException, Depends
from config.database import get_db
from core.security import create_access_token, create_refresh_token, verify_refresh_token
from models.users import User
from sqlalchemy.orm import Session

from services.otp_services import verify_otp_code



auth_router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)
@auth_router.get("/refresh")
async def fetch_token(refresh_token:str, db: Session = Depends(get_db)):
    payload = verify_refresh_token(refresh_token)
    user = db.query(User).filter(User.id == payload.get("sub")).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email
        }
    )
    return {
        "access_token": access_token,
        "type": "bearer"
    }
    

@auth_router.post('/verify_otp_code')
async def verify_otp(otp_code:str,user_id: int ,db: Session = Depends(get_db)):
    status = verify_otp_code(user_id=user_id, otp= otp_code)

    if not status:
        HTTPException(status_code=400, detail="Invalid or expired otp")

    user = db.query(User).filter(
            User.id == user_id
        ).first()
    

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    user.is_email_verified = True
    

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email
        }
    )

    refresh_token = create_refresh_token(
        data={
            "sub": str(user.id)
        }
    )

    db.commit()
    db.refresh(user)

    return {
        "message": "Email verified successfully",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

