from fastapi import APIRouter, status, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.database import get_db
from auth.services import get_token, get_refresh_token, verify_email_token, resend_email_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)

@router.post("/token", status_code=status.HTTP_200_OK)
async def authenticate_user(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await get_token(data=data, db=db)

@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_access_token(refresh_token: str = Header(), db: Session = Depends(get_db)):
    return await get_refresh_token(token=refresh_token, db=db)

@router.get("/verify", status_code=status.HTTP_200_OK)
async def verify_email(token: str, db: Session = Depends(get_db)):
    return await verify_email_token(token=token, db=db)

@router.post("/resend", status_code=status.HTTP_200_OK)
async def resend_email(email: str, db: Session = Depends(get_db)):
    return await resend_email_token(email=email, db=db)
