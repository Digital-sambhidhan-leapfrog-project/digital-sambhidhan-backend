from users.models import UserModel
from fastapi.exceptions import HTTPException
from core.security import get_password_hash
from datetime import datetime

async def create_user_account(data, db):
    """
    Create a new user account.

    Args:
        data: Data for creating a new user account.
        db: Database session.

    Returns:
        UserModel: The newly created user model.
        
    Raises:
        HTTPException: Raises HTTPException with status_code and detail if an error occurs.
    """
    user = db.query(UserModel).filter(UserModel.email == data.email).first()
    
    if user:
        if not user.is_verified:
            raise HTTPException(status_code=409, detail="Email address not verified")
        raise HTTPException(status_code=422, detail="Email is already registered and verified with us.")

    new_user = UserModel(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        password=get_password_hash(data.password),
        is_active=True,
        is_verified=False,
        registered_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
