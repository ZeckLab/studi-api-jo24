from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from jose import jwt, JWTError
from pydantic import ValidationError
from datetime import datetime

from src.core.models.User import User
from src.core.config import security
from src.core.config.database import get_db
from .constants import ErrorCode
from src.core.schemas.user_schema import UserEmailExist, UserInDB, UserRegister
from src.core.schemas.token_schema import Token, TokenPayload
from src.core.controllers import user_controller
from src.core.config import config
from src.core.config.security import authentication_mode

router = APIRouter()

'''Register a new user'''
@router.post("/signup", response_model=UserInDB)
async def signup(user_in: UserRegister, db=Depends(get_db)):
    """
    Register a new user
    """
    # check if the email of user already exists
    user = await user_controller.register_user(db, user_in)
    
    return UserInDB.model_validate(user)


@router.get("/login/{email}", response_model=UserEmailExist)
async def login(email: str, db: Session = Depends(get_db)):
    """
    Vérify if the email is already in the database
    """
    user_exist = UserEmailExist(email=email, exist=False)
    
    db_user = await user_controller.get_user_by_email(db, email)
    if db_user:
        user_exist.exist = True
    
    return user_exist


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login a user
    """
    db_user = await user_controller.get_user_by_email(db, form_data.username)
    
    if not security.verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ErrorCode.USER_INVALID_PASSWORD)

    elif not db_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorCode.USER_NOT_ACTIVE)
    
    access_token_expires = timedelta(minutes=config.JWT_EXPIRE)

    return Token(access_token=security.create_access_token({'sub':db_user.email}, expires_delta=access_token_expires))


'''Get the user logged in token'''
async def get_user_in_token(db: Session = Depends(get_db), token: str = Depends(authentication_mode)) -> User:
    '''Get the user logged in token
    :param db: the database session
    :param token: the token of the user
    :return: the user logged in token
    '''
    try:
        # decode the token
        payload = jwt.decode(
            token, config.JWT_SECRET, config.JWT_ALGO
        )
        
        token_data = TokenPayload(**payload)
        print("Temps", datetime.fromtimestamp(payload.get("exp")))
        
    except (JWTError, ValidationError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ErrorCode.USER_NOT_CREDENTIALS)
    
    # get the user by email
    user = await user_controller.get_user_by_email(db, token_data.sub)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.USER_NOT_FOUND)
    
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorCode.USER_NOT_ACTIVE)
    
    return user


'''Get the current admin user logged in token'''
def get_admin_in_token(user_in_token: User = Depends(get_user_in_token)) -> User:
    '''Get the current admin user logged in token
    :param user_in_token: the user logged in token
    :return: the current admin user logged in token
    '''
    
    if "admin" not in user_controller.get_user_roles(user_in_token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=ErrorCode.USER_NOT_CREDENTIALS
        )
    return user_in_token
