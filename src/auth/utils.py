from datetime import datetime, timedelta, timezone
from typing import TypedDict

import jwt
from pwdlib import PasswordHash

from env_vars import ACCESS_TOKEN_EXPIRY_MINUTES, ALGORITHM, SECRET_KEY

password_hasher = PasswordHash.recommended()


class JwtPayloadInput(TypedDict):
    sub: str


def get_hashed_password(password: str):
    return password_hasher.hash(password)


def verify_password(plaintext_password: str, hashed_password: str):
    return password_hasher.verify(plaintext_password, hashed_password)


def generate_token(data_to_be_encoded: JwtPayloadInput) -> str:
    issued_at = datetime.now(timezone.utc)
    expires_at = issued_at + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)

    payload = {
        **data_to_be_encoded,
        "exp": int(expires_at.timestamp()),
        "iat": int(issued_at.timestamp()),
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token
