from fastapi.security import OAuth2PasswordBearer

from env_vars import ACCESS_TOKEN_EXPIRY_MINUTES, ALGORITHM, SECRET_KEY

from .utils import generate_token, get_hashed_password, verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

__all__ = [
    "oauth2_scheme",
    "get_hashed_password",
    "verify_password",
    "generate_token",
    "ACCESS_TOKEN_EXPIRY_MINUTES",
    "ALGORITHM",
    "SECRET_KEY",
]
