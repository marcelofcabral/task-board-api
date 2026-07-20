import os

SECRET_KEY = os.environ["JWT_SECRET"]  # fail fast if missing
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRY_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRY_MINUTES", "60"))
