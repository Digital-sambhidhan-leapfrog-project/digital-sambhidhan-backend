from pydantic import BaseModel

class TokenResponse(BaseModel):
    """
    Pydantic model for the token response.
    """
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'
    expires_in: int
