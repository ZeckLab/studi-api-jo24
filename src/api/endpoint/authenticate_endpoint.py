from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.config.database import get_db
from .constants import ErrorCode
from src.core.schemas.user_schema import UserEmailExist, UserInDB, UserRegister
from src.core.controllers import user_controller

router = APIRouter()

'''Register a new user'''
@router.post("/signup", response_model=UserInDB)
async def signup(user_in: UserRegister, db=Depends(get_db)):
    """
    Register a new user
    """
    print("user_in",user_in)
    # check if the email of user already exists
    user = await user_controller.register_user(db, user_in)
    
    return UserInDB.model_validate(user)


@router.get("/login/{email}", response_model=UserEmailExist)
async def login(email: str, db: Session = Depends(get_db)):
    """
    Vérify if the email is already in the database
    """
    print("email_in",email)
    user_exist = UserEmailExist(email=email, exist=False)
    
    db_user = await user_controller.get_user_by_email(db, email)
    if db_user:
        print("User exist",db_user)
        user_exist.exist = True
    
    return user_exist