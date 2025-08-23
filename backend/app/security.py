from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from .config import get_settings
from .db import users


bearer_scheme = HTTPBearer(auto_error=False)


def create_access_token(subject: str, expires_minutes: Optional[int] = None) -> str:
	settings = get_settings()
	expires_delta = timedelta(minutes=expires_minutes or settings.access_token_expire_minutes)
	to_encode = {"sub": subject, "exp": datetime.utcnow() + expires_delta}
	return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


async def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme)) -> str:
	if credentials is None or credentials.scheme.lower() != "bearer":
		raise HTTPException(status_code=401, detail="Not authenticated")
	token = credentials.credentials
	settings = get_settings()
	try:
		payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
		subject = payload.get("sub")
		if not subject:
			raise HTTPException(status_code=401, detail="Invalid token")
		# validate subject exists
		user = users.get_by_email(subject)
		if user is None:
			raise HTTPException(status_code=401, detail="User not found")
		return subject
	except JWTError:
		raise HTTPException(status_code=401, detail="Invalid token")