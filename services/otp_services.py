import secrets
from services.redis_services import redis_client


def get_otp_code():
    return str(secrets.randbelow(900000)+100000)


def save_otp_code(email: str, otp:str):
    redis_client.setex(
        f"email_verify: {email}",
        1800,
        otp
    )

def verify_otp_code(email:str, otp: str):
    stored_otp = redis_client.get(
      f"email_verify: {email}"  
    )

    if stored_otp != otp:
        return False

    redis_client.delete(
     f"email_verify: {email}"     
    )

    return True

      