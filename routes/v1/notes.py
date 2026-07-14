from fastapi import APIRouter, Depends, HTTPException
from config.database import get_db
from sqlalchemy.orm import Session
from core.auth import get_current_user
from models.notes import Note
from models.users import User
from schemas.notes import NoteSchema, NoteSchemaOut, NoteSchemaUpdate

router = APIRouter(
    prefix="/notes",
    tags=["notes"]
)
@router.get("/fetch_notes")
async def get_notes( current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
   
    notes = db.query(Note).filter(Note.user_id == current_user.id).all()
    
    if not notes:
        raise HTTPException(status_code=404, detail="Notes not found")

    return notes


@router.post("/create_note")
async def create_note(note: NoteSchema, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_note = Note(
        title=note.title,
        content=note.content,
        user_id= current_user.id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return db_note

@router.delete("/delete_note/{note_id}")
async def delete_note(note_id: int, db: Session = Depends(get_db),    current_user: User = Depends(get_current_user),):
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"detail": "Note deleted successfully"}


@router.put("/update_note/{note_id}")
async def update_note(note_id: int, note: NoteSchemaUpdate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    existing_note = db.query(Note).filter(Note.id ==  note_id, Note.user_id == current_user.id).first()
    if not existing_note:
        raise HTTPException(status_code=404, detail="Note not found")
    for key, value in note.model_dump(exclude_unset=True).items():
        setattr(existing_note, key, value)
        setattr(existing_note, key, value)
    db.commit()
    db.refresh(existing_note)
    return existing_note
