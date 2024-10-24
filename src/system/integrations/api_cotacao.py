

import os
import logging
from typing import Optional
from requests import request
from datetime import datetime
from pydantic import BaseModel, field_validator

from requests.exceptions import HTTPError
from src.system.core.logger_core import logger


class ApiResponse(BaseModel):
    code: Optional[str] #"USD",
    codein: Optional[str] # "BRL",
    name: Optional[str] #"Dólar Americano/Real Brasileiro",
    high: Optional[float] #"5.734",
    low: Optional[float] #"5.7279",
    varBid: Optional[float] #"-0.0054",
    pctChange: Optional[float] #"-0.09",
    bid: Optional[float] #"5.7276",
    ask: Optional[float] #"5.7282",
    timestamp: Optional[str] #"1618315045",
    create_date: Optional[datetime] #"2021-04-13 08:57:27"

    @field_validator('create_date', mode="before")
    def parse_date_consult(cls, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            except ValueError as e:
                raise ValueError(f"O formato de data de retorno é inválido: {value}") from e
        return value
class FilterCotacao(BaseModel):
    moeda: str
    
    
class Cotacao():
    def __init__(self) -> None:
        """
        Inicializa a classe e configura a URL base para as cotações.

        Obtém a URL base da variável de ambiente 'COTACAO_BASE_URL'. Se a variável
        não estiver definida ou estiver vazia, uma exceção ValueError é levantada.
        """
        self.COTACAO_BASE_URL = os.environ.get("COTACAO_BASE_URL", "https://economia.awesomeapi.com.br/")
        if not self.COTACAO_BASE_URL:
            raise ValueError("A variável de ambiente 'COTACAO_BASE_URL' não está definida ou está vazia.")

    def get_cotacao(self, filter: FilterCotacao) -> ApiResponse:
        """
        Busca a cotação das moedas especificadas pelo filtro.

        Args:
            filter (FilterCotacao): Um objeto que contém informações sobre
                                    as moedas a serem consultadas.

        Raises:
            HTTPError: Levanta uma exceção se a resposta da requisição HTTP não
                    for bem-sucedida.
            Exception: Levanta uma exceção genérica para outros erros que possam
                    ocorrer durante o processamento.

        Returns:
            ApiResponse: Um objeto que contém os dados da cotação das moedas
                        consultadas.
        """
        try:
            url = f"{self.COTACAO_BASE_URL}last/{filter.moeda}"     
            # filters = filter.model_dump(exclude_none=True)
            response = request(url=url, method="GET")
            response.raise_for_status()
            return ApiResponse.model_validate(response.json().get(self._remove_symbol(text=filter.moeda, symbol="-")))
        except HTTPError as error:
            logger(mensagem=f"get_store_mercado_bitcoin -> {error}", nivel=logging.ERROR)
            raise error
        except Exception as error:
            logger(mensagem=f"get_store_mercado_bitcoin -> {error}", nivel=logging.ERROR)
            raise error

    def _remove_symbol(self, text: str, symbol: str) -> str:
        """
        Remove um símbolo específico de uma string.

        Args:
            text (str): A string da qual o símbolo deve ser removido.
            symbol (str): O símbolo a ser removido da string.

        Returns:
            str: A string resultante após a remoção do símbolo.
        """
        return text.replace(f"{symbol}", "")
