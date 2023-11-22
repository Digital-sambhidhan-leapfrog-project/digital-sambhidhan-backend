from fastapi import APIRouter, status, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from core.database import get_db
from users.schemas import CreateUserRequest
from users.services import create_user_account
from core.security import oauth2_scheme
from users.responses import UserResponse
from auth.services import send_activation_email

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)]
)

@router.post('', status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUserRequest, db: Session = Depends(get_db)):
    """
    Create a new user account.

    Args:
        data (CreateUserRequest): Request data for creating a user.
        db (Session): Database session.

    Returns:
        JSONResponse: JSON response with a success message.
    """
    new_user = await create_user_account(data=data, db=db)
    await send_activation_email(new_user.email)
    payload = {"message": "User account has been successfully created. Please check your email to verify your account."}
    return JSONResponse(content=payload)

@user_router.post('/me', status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user_detail(request: Request):
    """
    Get user details.

    Args:
        request (Request): The HTTP request.

    Returns:
        UserResponse: User details.
    """
    return request.user
