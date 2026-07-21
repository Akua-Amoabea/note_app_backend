from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from schemas.users import UserSchema, CurrentUserSchema, UserSchemaOut
from config.database import get_db
from sqlalchemy.orm import Session
from models.users import PendingUser, User
from core.security import create_access_token, create_refresh_token, hash_password, verify_password, verify_refresh_token, verify_token
from services.email_services import send_verification_email
from services.otp_services import get_otp_code, save_otp_code, verify_otp_code


user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@user_router.post("/create_user")
async def create_user(user: UserSchema, db: Session = Depends(get_db)):

    email = user.email.strip().lower()
    password = user.password.strip().lower()

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
    
    user_password = hash_password(password=password)

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
        "id": db_user.id,
        "first_name": db_user.first_name,
        "last_name": db_user.last_name,
        "email": db_user.email
    }

@user_router.post("/login")
async def fetch_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    email = form_data.username.strip().lower()
    password = form_data.password.strip().lower()

    current_user = db.query(User).filter(
        User.email == email
    ).first()


    # 1. Check if user exists first
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )

    # 3. Check password
    if not verify_password(
        password,
        current_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )


    # 4. Create tokens
    access_token = create_access_token(
        data={
            "sub": str(current_user.id),
            "email": current_user.email
        }
    )


    refresh_token = create_refresh_token(
        data={
            "sub": str(current_user.id)
        }
    )


    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }



@user_router.post("/reset_password")
async def reset_password(email: str ,old_password: str, new_password: str ,db: Session = Depends(get_db)):
    trimmed_email = email.strip().lower()
    trimmed_old_password = old_password.strip().lower()
    trimmed_new_password = new_password.strip().lower()

    existing_user = db.query(User).filter(User.email == trimmed_email).first()

    if not existing_user:
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    

    result = verify_password(trimmed_old_password, existing_user.password)

    if not result:
       raise HTTPException(status_code=400, detail="Incorrect password")

    change_password = hash_password(trimmed_new_password)

    existing_user.password = change_password

    db.commit()
    db.refresh(existing_user)

    return {
        "message": "password changed successfully"
    }



