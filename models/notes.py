from config.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class Note(Base):
    __tablename__ = "notes"

    id= Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)






