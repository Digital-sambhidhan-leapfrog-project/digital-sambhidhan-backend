from pydantic import BaseModel, EmailStr
from typing import Union
from datetime import datetime

class BaseResponse(BaseModel):
    """
    Base class for response Pydantic models.
    """
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class UserResponse(BaseResponse):
    """
    Pydantic model for user response.

    Attributes:
        id (int): User ID.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        email (EmailStr): Email address of the user.
        registered_at (Union[None, datetime]): Date and time when the user registered.
    """
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    registered_at: Union[None, datetime] = None
