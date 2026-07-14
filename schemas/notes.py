from pydantic import BaseModel

class NoteSchema(BaseModel):
    title: str
    content: str
    user_id: int


class NoteSchemaOut(BaseModel):
    user_id: int
    title: str
    content: str  


class NoteSchemaUpdate(BaseModel):
    title: str
    content: str

