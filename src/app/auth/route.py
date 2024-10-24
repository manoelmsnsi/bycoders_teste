from typing import Annotated
from fastapi import Depends,APIRouter,  HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.app.auth.model import User, UserInDB
from src.app.auth.controller import AuthController


#CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG#
backend = APIRouter()

auth_controller = AuthController()

@backend.post("/token", tags=["AUTH"])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Realiza o login de um usuário e gera um token de acesso.

    Args:
        form_data (OAuth2PasswordRequestForm): Os dados do formulário de
                                                login, incluindo nome de 
                                                usuário e senha.

    Raises:
        HTTPException: Levanta uma exceção 401 se o usuário não for encontrado 
                       ou se a senha estiver incorreta.

    Returns:
        dict: Um dicionário contendo o token de acesso e o tipo do token.
    """
    user_dict = auth_controller.get_user(username=form_data.username)
    if not user_dict:
        raise HTTPException(status_code=401, detail="Unauthorized")    
    user = UserInDB.model_validate(user_dict.model_dump())
    hashed_password = auth_controller.fake_hash_password(form_data.password)
    if hashed_password != user.hashed_password:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    return {"access_token": user.username, "token_type": "bearer"}

@backend.get("/users/me", response_model=User, tags=["AUTH"])
async def read_users_me(current_user: Annotated[User, Depends(auth_controller.get_current_user)]):
    """
    Obtém as informações do usuário atualmente autenticado.

    Args:
        current_user (User): O usuário autenticado, que é obtido
                             a partir do token de acesso.

    Returns:
        User: O objeto User que representa o usuário autenticado.
    """
    return current_user
