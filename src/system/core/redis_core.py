import json
import os
import redis.asyncio as redis  

class RedisCore():
    def __init__(self) -> None:
        self.REDIS_HOST = os.environ.get("REDIS_HOST", "0.0.0.0")
        self.REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
        self.REDIS_TIME = int(os.environ.get("REDIS_TIME", 3600))
        
        try:
            self.redis_service = redis.StrictRedis(host=f"{self.REDIS_HOST}", port=self.REDIS_PORT, db=5,decode_responses=True,retry_on_timeout=True)
        except redis.ConnectionError as e:
            print(f"Erro de conexão com o Redis: {e}")        
        except redis.TimeoutError as e:
            print(f"Erro de timeout ao conectar ao Redis: {e}")        
        except Exception as e:
            print(f"Ocorreu um erro ao tentar conectar ao Redis: {e}")

    async def set_redis(self, key, data):
        """
        Armazena dados no Redis com a chave especificada.

        Args:
            key (str): A chave sob a qual os dados serão armazenados no Redis.
            data (Any): Os dados a serem armazenados.

        Returns:
            bool: Retorna True se os dados foram armazenados com sucesso, 
                caso contrário, lança uma exceção.
        """
        try:
            return await self.redis_service.set(key, data)
        except Exception as error:
            raise Exception(error)

    async def get_redis(self, key):
        """
        Recupera dados do Redis usando a chave especificada.

        Args:
            key (str): A chave para recuperar os dados armazenados.

        Returns:
            Any: Retorna os dados armazenados como um dicionário, ou 
                uma lista vazia se não houver dados.
        """
        try:
            response = await self.redis_service.get(key)
            if response:
                return json.loads(response)
            return []
        except Exception as error:
            raise Exception(error)

    async def expire_redis(self, key, time=None):
        """
        Define um tempo de expiração para a chave especificada no Redis.

        Args:
            key (str): A chave para a qual o tempo de expiração será definido.
            time (int, optional): O tempo de expiração em segundos. Se None, 
                                usa o tempo padrão definido em REDIS_TIME.

        Returns:
            bool: Retorna True se a expiração foi definida com sucesso, 
                caso contrário, lança uma exceção.
        """
        try:
            if time is None:
                time = self.REDIS_TIME  
            return await self.redis_service.expire(key, time, nx=True)
        except Exception as error:
            raise Exception(error)

    async def incr_redis(self, key):
        """
        Incrementa o valor armazenado na chave especificada no Redis.

        Args:
            key (str): A chave do valor a ser incrementado.

        Returns:
            int: O novo valor após o incremento, caso tenha sucesso.
        """
        try:
            return await self.redis_service.incr(key)
        except Exception as error:
            raise Exception(error)

    async def decr_redis(self, key):
        """
        Decrementa o valor armazenado na chave especificada no Redis.

        Args:
            key (str): A chave do valor a ser decrementado.

        Returns:
            int: O novo valor após o decremento, caso tenha sucesso.
        """
        try:
            return await self.redis_service.decr(key)
        except Exception as error:
            raise Exception(error)

    async def setnx_redis(self, key, data):
        """
        Armazena dados no Redis apenas se a chave especificada não existir.

        Args:
            key (str): A chave sob a qual os dados serão armazenados, 
                    se não existir no Redis.
            data (Any): Os dados a serem armazenados.

        Returns:
            bool: Retorna True se os dados foram armazenados com sucesso, 
                caso contrário, lança uma exceção.
        """
        try:
            return await self.redis_service.setnx(key, data)
        except Exception as error:
            raise Exception(error)
