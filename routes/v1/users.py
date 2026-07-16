from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from schemas.users import UserSchema, CurrentUserSchema, UserSchemaOut
from config.database import get_db
from sqlalchemy.orm import Session
from models.users import User
from core.security import create_access_token, create_refresh_token, hash_password, verify_password, verify_refresh_token, verify_token


user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@user_router.post("/create_user")
async def create_user(user: UserSchema, db: Session = Depends(get_db)):

    email = user.email.lower()
    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,    
            detail="Email already exists"
        )
    
    user_password = hash_password(user.password)

    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=email,
        password= user_password      
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {
        "id": db_user.id,
        "first_name": db_user.first_name,
        "last_name": db_user.last_name,
        "email": db_user.email
    }


@user_router.post("/login")
async def fetch_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    email = form_data.username.lower()
    current_user = db.query(User).filter(User.email == email).first()
    if not current_user:
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    
    if not verify_password(
        form_data.password,
        current_user.password

    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )
    
    access_token = create_access_token(
        data={
            "sub": str(current_user.id),
            "email": current_user.email
        }
    )


    refresh_token = create_refresh_token(
        data={
            "sub": str(current_user.id),
        }
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@user_router.get("/refresh")
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
    
