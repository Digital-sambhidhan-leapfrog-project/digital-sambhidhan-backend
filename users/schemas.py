from pydantic import BaseModel, EmailStr

class CreateUserRequest(BaseModel):
    """
    Pydantic model for creating a new user account.

    Attributes:
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        email (EmailStr): Email address of the user.
        password (str): Password for the user.
    """
    first_name: str
    last_name: str
    email: EmailStr
    password: str
