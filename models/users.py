from datetime import datetime, timedelta
from config.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime

class User(Base):
    __tablename__ = "users"

    id= Column(Integer, primary_key=True, index=True)
    first_name =Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  
    


class PendingUser(Base):
    __tablename__ = "pending_users"
    id= Column(Integer, primary_key=True, index=True)
    first_name =Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  
    expires_at = Column(DateTime, nullable=False)


