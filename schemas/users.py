from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
   

class UserSchemaOut(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

class CurrentUserSchema(BaseModel):
    email: EmailStr
    password: str
