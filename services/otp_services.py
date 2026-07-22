import secrets
from services.redis_services import redis_client
from redis.exceptions import RedisError
from fastapi import HTTPException


def get_otp_code():
    return str(secrets.randbelow(900000)+100000)


def save_otp_code(email: str, otp:str):
    try:
        redis_client.setex(
            f"email_verify: {email}",
            1800,
            otp
        )

    except RedisError:
            raise HTTPException(
              status_code= 503,
        detail="OTP service temporarily unavailable"   
            )
        

def verify_otp_code(email:str, otp: str):
    try:
        stored_otp = redis_client.get(
        f"email_verify: {email}"  
        )

        if stored_otp != otp:
            return False

        redis_client.delete(
        f"email_verify: {email}"     
        )

        return True
    
    except RedisError:
            raise HTTPException(
              status_code= 503,
        detail="OTP service temporarily unavailable"   
            )


     