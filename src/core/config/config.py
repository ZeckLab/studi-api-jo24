from starlette.config import Config

config = Config(".env")

JWT_EXPIRE: int = 60 * 24 * 2
JWT_ALGO: str = config("ALGORITHM")
JWT_SECRET: str = config("SECRET_KEY")

DATABASE_URI = config("DATABASE_URL")

ADMIN_EMAIL = config("ADMIN_EMAIL")
ADMIN_PASSWORD = config("ADMIN_PASSWORD")