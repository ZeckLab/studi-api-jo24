import random
import string
from fastapi.testclient import TestClient
from fastapi import Depends

from main import app
from src.core.config.database import get_db
from src.core.schemas.user_schema import UserVerify

def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


'''def test_get_existing_user_email() -> None:
    email = random_email()
    r = TestClient.get(app, f"http://localhost:4200/api/login/{email}")
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = api_user["exist"]
    assert existing_user'''