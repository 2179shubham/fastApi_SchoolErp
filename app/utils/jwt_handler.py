from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status
from app.config.auth_config import auth_settings

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    try:
        encoded_jwt = jwt.encode(
            to_encode, 
            auth_settings.SECRET_KEY, 
            algorithm=auth_settings.ALGORITHM
        )
        return encoded_jwt
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not create token"
        )

def verify_token(token: str) -> dict:
    try:
        print("Verifying token:", token)
        payload = jwt.decode(
            token, 
            auth_settings.SECRET_KEY, 
            algorithms=[auth_settings.ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )