from starlette.config import Config

config = Config(".env")

JWT_EXPIRE: int = 60 * 24 * 2
JWT_ALGO: str = config("ALGORITHM")
JWT_SECRET: str = config("SECRET_KEY")

DATABASE_URI = config("DATABASE_URL")

ADMIN_EMAIL = config("ADMIN_EMAIL")
ADMIN_PASSWORD = config("ADMIN_PASSWORD")

USER_WEB_APPLICATION_NAME_ROLE: str = 'user'
USER_WEB_APPLICATION_DESC_ROLE: str = 'User of the web application'

ADMIN_WEB_APPLICATION_NAME_ROLE: str = 'admin'
ADMIN_WEB_APPLICATION_DESC_ROLE: str = 'All permissions'

LIMIT_DISPLAY_ORDERS = 2
