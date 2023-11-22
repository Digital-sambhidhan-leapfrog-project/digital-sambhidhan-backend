from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from starlette.authentication import AuthCredentials, UnauthenticatedUser
from datetime import timedelta, datetime
from jose import jwt, JWTError
from core.config import get_settings
from fastapi import Depends
from core.database import get_db
from users.models import UserModel

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_password_hash(password):
    """
    Get the hashed version of a password.

    Args:
        password (str): The plaintext password.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """
    Verify a plaintext password against its hashed version.

    Args:
        plain_password (str): The plaintext password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the password is verified, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

async def create_access_token(data, expiry: timedelta):
    """
    Create an access token.

    Args:
        data (dict): The data to be included in the token payload.
        expiry (timedelta): The expiration time for the token.

    Returns:
        str: The access token.
    """
    payload = data.copy()
    expire_in = datetime.utcnow() + expiry
    payload.update({"exp": expire_in})
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

async def create_refresh_token(data):
    """
    Create a refresh token.

    Args:
        data (dict): The data to be included in the token payload.

    Returns:
        str: The refresh token.
    """
    return jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def get_token_payload(token):
    """
    Get the payload of a JWT token.

    Args:
        token (str): The JWT token.

    Returns:
        dict: The token payload.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        return None
    return payload

def get_current_user(token: str = Depends(oauth2_scheme), db=None):
    """
    Get the current user based on the JWT token.

    Args:
        token (str): The JWT token.
        db: The database session.

    Returns:
        UserModel: The user model if the token is valid, otherwise None.
    """
    payload = get_token_payload(token)
    if not payload or type(payload) is not dict:
        return None

    user_id = payload.get('id', None)
    if not user_id:
        return None

    if not db:
        db = next(get_db())

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    return user

def generate_activation_token(email):
    """
    Generate an activation token for email verification.

    Args:
        email (str): The email address.

    Returns:
        str: The activation token.
    """
    return jwt.encode({"email": email}, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

class JWTAuth:
    """
    FastAPI JWT authentication class.
    """

    async def authenticate(self, conn):
        """
        Authenticate a connection using JWT.

        Args:
            conn: The connection.

        Returns:
            Tuple: AuthCredentials and User.
        """
        guest = AuthCredentials(['unauthenticated']), UnauthenticatedUser()

        if 'authorization' not in conn.headers:
            return guest

        token = conn.headers.get('authorization').split(' ')[1]  # Bearer token_hash
        if not token:
            return guest

        user = get_current_user(token=token)

        if not user:
            return guest

        return AuthCredentials('authenticated'), user
