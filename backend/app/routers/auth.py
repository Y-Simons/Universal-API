from fastapi import APIRouter, Depends, HTTPException

from ..db import users, InMemoryUser
from ..models import Token, UserLogin, User
from ..security import create_access_token, get_current_user


router = APIRouter()


@router.post("/login", response_model=Token)
async def login(payload: UserLogin) -> Token:
	user = users.get_by_email(payload.email)
	if user is None or not users.verify_password(payload.password, user.password_hash):
		raise HTTPException(status_code=401, detail="Invalid credentials")
	token = create_access_token(user.email)
	return Token(access_token=token)


@router.get("/me", response_model=User)
async def me(current_email: str = Depends(get_current_user)) -> User:
	user: InMemoryUser = users.get_by_email(current_email)  # type: ignore
	return User(id=user.id, email=user.email, full_name=user.full_name, role=user.role)  # type: ignore