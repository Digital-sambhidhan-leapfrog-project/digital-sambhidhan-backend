from datetime import timedelta
from fastapi_mail import FastMail, MessageSchema, MessageType
from fastapi.exceptions import HTTPException

from core.config import get_settings, mail_conf
from core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    get_token_payload,
    generate_activation_token,
)

from auth.responses import TokenResponse
from users.models import UserModel


async def get_token(data, db):
    """
    Get the access and refresh tokens for the user based on the provided credentials.

    Args:
        data (dict): User credentials (username and password).
        db: Database session.

    Returns:
        TokenResponse: Access and refresh tokens.

    Raises:
        HTTPException: If the email is not registered or invalid login credentials.
    """
    user = db.query(UserModel).filter(UserModel.email == data.username).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Email is not registered with us.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid Login Credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    _verify_user_access(user=user)

    return await _get_user_token(user=user)


async def get_refresh_token(token, db):
    """
    Get a new access token using a refresh token.

    Args:
        token (str): Refresh token.
        db: Database session.

    Returns:
        TokenResponse: Access and refresh tokens.

    Raises:
        HTTPException: If the refresh token is invalid.
    """
    payload = get_token_payload(token=token)
    user_id = payload.get('id', None)

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return await _get_user_token(user=user, refresh_token=token)


def _verify_user_access(user: UserModel):
    """
    Verify user access by checking if the account is active and verified.

    Args:
        user: User model.

    Raises:
        HTTPException: If the account is inactive or unverified.
    """
    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Your account is inactive. Please contact support.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=400,
            detail="Your account is unverified. We have resent the account verification email.",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def _get_user_token(user: UserModel, refresh_token=None):
    """
    Generate access and refresh tokens for the user.

    Args:
        user: User model.
        refresh_token (str): Refresh token.

    Returns:
        TokenResponse: Access and refresh tokens.
    """
    payload = {"id": user.id}
    access_token_expiry = timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(payload, access_token_expiry)

    if not refresh_token:
        refresh_token = await create_refresh_token(payload)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=access_token_expiry.seconds  # in seconds
    )


async def send_activation_email(email: str):
    """
    Send an account activation email to the specified email address.

    Args:
        email (str): User's email address.
    """
    token = generate_activation_token(email)
    body = f"Activate your Smart Lawyer account using this link: <a href=localhost:8000/auth/verify?token={token}>Click here</a>"
    message = MessageSchema(
        subject="Activate your account",
        recipients=[email],
        body=body,
        subtype=MessageType.html
    )
    fm = FastMail(mail_conf)
    await fm.send_message(message)


async def verify_email_token(token, db):
    """
    Verify the email verification token and update the user's status.

    Args:
        token (str): Email verification token.
        db: Database session.

    Returns:
        dict: Success message.

    Raises:
        HTTPException: If the token is invalid or the email is not registered.
    """
    payload = get_token_payload(token)

    if not payload or type(payload) is not dict:
        raise HTTPException(
            status_code=400,
            detail="Invalid token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    email = payload.get('email', None)

    if not email:
        raise HTTPException(
            status_code=400,
            detail="Invalid token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(UserModel).filter(UserModel.email == email).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.is_verified:
        raise HTTPException(
            status_code=400,
            detail="Email is already verified.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user.is_verified = True
    db.commit()
    db.refresh(user)

    return {"message": "Email has been verified."}


async def resend_email_token(email, db):
    """
    Resend the email verification token to the user.

    Args:
        email (str): User's email address.
        db: Database session.

    Returns:
        dict: Success message.

    Raises:
        HTTPException: If the email is not registered or already verified.
    """
    user = db.query(UserModel).filter(UserModel.email == email).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Email is not registered with us.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.is_verified:
        raise HTTPException(
            status_code=400,
            detail="Email is already verified.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    await send_activation_email(email)

    return {"message": "Email verification token has been sent."}
