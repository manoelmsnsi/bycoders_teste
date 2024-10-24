import os
import logging
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from curl_cffi import requests
from requests.exceptions import HTTPError
from src.system.core.logger_core import logger

class FilterGetPerSymbol(BaseModel):
    symbol:str
    limit: Optional[int] = 20
    offset: Optional[int] = 0
    order: Optional[str] = 'desc'
    sort: Optional[str] = 'release_date'
    
class StoreMercadoBitcoin():
    def __init__(self) -> None:
        self.STORE_MERCADO_BITCOIN_BASE_URL=os.environ.get("STORE_MERCADO_BITCOIN_BASE_URL","https://store.mercadobitcoin.com.br/api/v1/")        
        if not self.STORE_MERCADO_BITCOIN_BASE_URL:
            raise ValueError("A variável de ambiente 'STORE_MERCADO_BITCOIN_BASE_URL' não está definida ou está vazia.")

    def get_per_symbol(self, symbol: str) :
        """_summary_
            Args:
                filter (FilterStoreMercadoBitCoin): 
                    limit: int = 20
                    offset: int = 0
                    order: str = 'desc'
                    sort: str = 'release_date'

            Raise:
                error: HTTPError
                error: Exception

            Returns:
                ApiResponse:{}
        """
        try:            
            url=f"{self.STORE_MERCADO_BITCOIN_BASE_URL}marketplace/product/unlogged"     
            filters = FilterGetPerSymbol(symbol=symbol).model_dump()
            response = requests.get(url=url,params=filters, impersonate="chrome")
            response.raise_for_status()
            response_data = response.json()
            product = response_data['response_data']['products'][0]  # Assumindo que há pelo menos 1 produto
            response_formatted= {
                'coin_name': product['name'],
                'symbol': symbol, 
                'coin_price': float(product['market_price']),  
                'coin_price_dolar': float(0.0),  
                'date_consult': datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
            }
            return response_formatted
        except HTTPError as error:
            logger(mensagem=f"get_store_mercado_bitcoin -> {error}",nivel=logging.ERROR)
            raise error
        except Exception as error:
            logger(mensagem=f"get_store_mercado_bitcoin -> {error}",nivel=logging.ERROR)
            raise error