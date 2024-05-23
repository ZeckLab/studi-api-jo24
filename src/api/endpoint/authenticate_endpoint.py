from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.core.security import security
from src.core.config.database import get_db
from .constants import ErrorCode
from src.core.schemas.user_schema import UserEmailExist, UserInDB, UserRegister, UserLogin, UserInResponse
from src.core.schemas.token_schema import Token
from src.core.controllers import user_controller
from src.core.config import config

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

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login a user
    """
    print("form_data",form_data)
    db_user = await user_controller.get_user_by_email(db, form_data.username)
    
    if not security.verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ErrorCode.INVALID_EMAIL_OR_PASSWORD)
    elif not db_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorCode.USER_NOT_ACTIVE)
    
    access_token_expires = timedelta(minutes=config.JWT_EXPIRE)
    return Token(access_token=security.create_access_token({'sub':db_user.email}, expires_delta=access_token_expires))