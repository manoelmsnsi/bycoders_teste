import os
import requests
from datetime import datetime

class CoinGecko():
    def __init__(self) -> None:
        self.COINGECKO_BASE_URL=os.environ.get("COINGECKO_BASE_URL","https://api.coingecko.com/api/v3/")
        if not self.COINGECKO_BASE_URL:
            raise ValueError("A variável de ambiente 'COINGECKO_BASE_URL' não está definida ou está vazia.")
        self.crypto_symbols = self.get_crypto_symbols()
        
    def get_crypto_symbols(self):
        """
        Busca todos os símbolos de criptomoedas e retorna um dicionário
        que mapeia o símbolo da criptomoeda ao seu ID.

        Returns:
            dict: Um dicionário onde as chaves são os símbolos das 
                criptomoedas e os valores são os IDs correspondentes.

        Raises:
            Exception: Se a requisição à API falhar ou retornar um código
                    de status diferente de 200.
        """
        url = f"{self.COINGECKO_BASE_URL}coins/list"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Erro ao acessar a API: {response.status_code} - {response.text}")

        return {coin['symbol']: coin['id'] for coin in response.json()}

    def get_per_symbol(self, symbol, vs_currency='usd'):
        """
        Busca os dados da criptomoeda pelo símbolo especificado e retorna
        informações formatadas sobre a criptomoeda.

        Args:
            symbol (str): O símbolo da criptomoeda para a qual os dados 
                        devem ser buscados.
            vs_currency (str, optional): A moeda em que o preço da 
                                        criptomoeda será retornado. 
                                        O padrão é 'usd'.

        Returns:
            dict: Um dicionário contendo informações sobre a criptomoeda, incluindo 
                nome, símbolo, preço atual e data da consulta.

        Raises:
            Exception: Se a criptomoeda com o símbolo especificado não for encontrada 
                    ou se a requisição à API falhar ou retornar um código de 
                    status diferente de 200.
        """
        coin_id = self.crypto_symbols.get(symbol)
        if not coin_id:
            raise Exception(f"Criptomoeda com símbolo '{symbol}' não encontrada.")
        url = f"{self.COINGECKO_BASE_URL}coins/{coin_id}"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Erro ao acessar a API: {response.status_code} - {response.text}")

        response_data = response.json()
        response_formatted = {
            'coin_name': response_data['name'],
            'symbol': response_data['symbol'],
            'coin_price': response_data['market_data']['current_price'][vs_currency],
            'coin_price_dolar': response_data['market_data']['current_price']['usd'],
            'date_consult': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        return response_formatted



