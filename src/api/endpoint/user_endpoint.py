from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status

from src.api.endpoint.authenticate_endpoint import get_user_in_token
from src.core.config.database import get_db
from src.core.config.security import authentication_mode
from .constants import ErrorCode
from src.core.schemas.user_schema import RoleBase, RoleInDB
from src.core.controllers import user_controller


router = APIRouter()

'''Add a new role'''
@router.post("/role", response_model=RoleInDB)
async def add_role(role_in: RoleBase, db=Depends(get_db)) -> Any:
    """
    Add a new role
    """
    #check if the role already exists
    role_name_exist = await user_controller.get_role_by_name(db, role_in.name)

    if role_name_exist is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorCode.ROLE_NAME_ALREADY_EXISTS)
    
    # add the role
    role_in_db : RoleInDB = await user_controller.create(db, role_in)
    
    return role_in_db


'''Get the roles of the user connected in the token'''
@router.get("/me/roles", dependencies=[Depends(authentication_mode)], response_model=list[str])
def get_roles_user(db=Depends(get_db), user= Depends(get_user_in_token)) -> Any:
    """
    Get the list of roles for the user connected
    """
    if(user is None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    roles = user_controller.get_user_roles(user)
    return roles
