from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status

from src.core.config.database import get_db

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
