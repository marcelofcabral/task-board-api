from fastapi.security import OAuth2PasswordBearer

from env_vars import ACCESS_TOKEN_EXPIRY_MINUTES, ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

__all__ = [
    "ACCESS_TOKEN_EXPIRY_MINUTES",
    "ALGORITHM",
    "SECRET_KEY",
    "oauth2_scheme",
]
