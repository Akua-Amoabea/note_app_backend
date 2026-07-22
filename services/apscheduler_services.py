from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import Depends

from config.database import get_db
from sqlalchemy.orm import Session
from models.users import PendingUser


def delete_pending_users():
    db = next(get_db())

    try:
        users =  db.query(PendingUser).filter(PendingUser.expires_at < datetime.now()).all()
        for user in users:
            db.delete(user)

        db.commit()    
        print('deletion completed successfully')

    finally:
        db.close()    

scheduler = AsyncIOScheduler()


def run_scheduler():
    scheduler.add_job(delete_pending_users, "cron", hour=23)
    scheduler.start()

    