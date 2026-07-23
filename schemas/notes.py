from pydantic import BaseModel

class NoteSchema(BaseModel):
    title: str
    content: str


class NoteSchemaOut(BaseModel):
    id:str
    title: str
    content: str  


class NoteSchemaUpdate(BaseModel):
    title: str
    content: str

