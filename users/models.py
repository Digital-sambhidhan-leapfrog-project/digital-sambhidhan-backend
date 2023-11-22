from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from datetime import datetime

from core.database import Base

class UserModel(Base):
    """
    User model for storing user information.

    Attributes:
        id (int): Primary key for the user.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        email (str): Email address of the user (unique).
        password (str): Hashed password of the user.
        is_active (bool): Indicates if the user account is active.
        is_verified (bool): Indicates if the user email is verified.
        verified_at (DateTime): Date and time when the email was verified.
        registered_at (DateTime): Date and time when the user registered.
        updated_at (DateTime): Date and time when the user record was last updated.
        created_at (DateTime): Date and time when the user record was created.
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(100))
    is_active = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True, default=None)
    registered_at = Column(DateTime, nullable=True, default=None)
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
