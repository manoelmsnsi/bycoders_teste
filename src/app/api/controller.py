import logging
from fastapi import HTTPException
from src.system.core.logger_core import logger
from src.app.api.model import ApiOut, ApiFilter
from src.system.core.redis_core import RedisCore
from src.system.integrations.api_coin_gecko import CoinGecko
from src.system.integrations.api_cotacao import Cotacao, FilterCotacao
from src.system.integrations.api_store_mercado_bitcoin import StoreMercadoBitcoin

class ApiController():   
    def __init__(self):
        self.cotacao_integration = Cotacao()
        self.redis_core = RedisCore()
        self.CLASS_MAPPING = {
            "StoreMercadoBitcoin":StoreMercadoBitcoin(),
            "CoinGecko":CoinGecko(),
        }
    async def search_coin_per_symbol(self, data: ApiFilter) -> ApiOut:
            api_response=None
            reponse_redis = await self.redis_core.get_redis(key=data.symbol)            
            if reponse_redis:
                logger(mensagem=":D -------- REDIS CACHED -------- :D",nivel=logging.WARNING)
                return ApiOut(**reponse_redis)
            for class_integracao in self.CLASS_MAPPING:
                try:
                    api_response = ApiOut(**self.CLASS_MAPPING.get(class_integracao).get_per_symbol(symbol=data.symbol))
                    break
                except Exception as error:
                    logger(mensagem=f":( Erro na consulta da integração {class_integracao} :(",nivel=logging.WARNING)
            if not api_response:
                raise HTTPException(status_code=404, detail="Symbol não encontrado.")
            if api_response.coin_price_dolar==0.0:
                response_cotacao = self.cotacao_integration.get_cotacao(
                    filter=FilterCotacao(moeda="USD-BRL")
                )                
                api_response.coin_price_dolar=response_cotacao.high * float(api_response.coin_price)

            await self.redis_core.setnx_redis(key=data.symbol, data=api_response.model_dump_json())
            await self.redis_core.expire_redis(key=data.symbol)
            logger(mensagem=":D -------- SEND CACHED -------- :D",nivel=logging.INFO)
            return api_response

