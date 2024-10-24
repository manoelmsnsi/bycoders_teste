from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from src.app.auth.model import User
from src.app.api.model import ApiFilter, ApiOut
from src.app.api.controller import ApiController
from src.app.auth.controller import AuthController


#CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG#
backend = APIRouter()

api_controller= ApiController()
auth_controller = AuthController()

#BACKEND-BACKEND-BACKEND-BACKEND-BACKEND-BACKEND-BACKEND-BACKEND-BACKEND-BACKEND-BACKEND-BACKEND-BACKEND-BACKEND-BACKEND-BACKEND-BACKEND-BACKEND-BACKEND-BACKEND#
@backend.get("/api",response_model=ApiOut, tags=["SEARCH"])
async def get_coin_per_symbo(current_user: Annotated[User, Depends(auth_controller.get_current_user)],data:Annotated[ApiFilter,Depends()],):  
    result = jsonable_encoder( await api_controller.search_coin_per_symbol(data=data))    
    return result

