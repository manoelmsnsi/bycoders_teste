from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.app.auth.model import  UserInDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AuthController:
    def __init__(self) -> None:
        """
        Inicializa a classe e configura um banco de dados simulado de usuários.

        O banco de dados contém usuários fictícios com informações como nome de 
        usuário, nome completo, e-mail, senha hash e status de desativação.
        """
        self.fake_users_db = {
            "teste": {
                "username": "teste",
                "full_name": "teste teste",
                "email": "teste@example.com",
                "hashed_password": "fakehashedteste",
                "disabled": False,
            },
            "alice": {
                "username": "alice",
                "full_name": "Alice Wonderson",
                "email": "alice@example.com",
                "hashed_password": "fakehashedsecret",
                "disabled": True,
            },
        }

    @staticmethod
    def fake_hash_password(password: str) -> str:
        """
        Simula o hashing de uma senha.

        Args:
            password (str): A senha a ser hashada.

        Returns:
            str: A senha hashada simulada, prefixada com "fakehashed".
        """
        return "fakehashed" + password

    def get_user(self, username: str) -> UserInDB:
        """
        Obtém um usuário do banco de dados simulado com base no nome de usuário.

        Args:
            username (str): O nome de usuário do usuário a ser buscado.

        Returns:
            UserInDB: Um objeto UserInDB correspondente ao usuário, ou None
                    se o usuário não for encontrado.
        """
        user_dict = self.fake_users_db.get(username)
        if user_dict:
            return UserInDB(**user_dict)
        return None

    def fake_decode_token(self, token: str) -> UserInDB:
        """
        Simula a decodificação de um token para recuperar o usuário associado.

        Args:
            token (str): O token a ser decodificado.

        Returns:
            UserInDB: Um objeto UserInDB correspondente ao usuário associado
                    ao token.
        """
        return self.get_user(token)

    def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
        """
        Obtém o usuário atual a partir do token fornecido.

        Args:
            token (str): O token de autenticação do usuário.

        Raises:
            HTTPException: Levanta uma exceção 401 se o token não for válido
                        ou se o usuário estiver desativado.

        Returns:
            UserInDB: O objeto UserInDB correspondente ao usuário atual.
        """
        user = self.fake_decode_token(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if user.disabled:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return user
