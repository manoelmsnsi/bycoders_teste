
## TESTE - MANOEL MESSIAS DA SILVA NETO

Essa aplicação foi construída em Python, utilizando , Redis para cache, request e curl-cffi, para requisição. A aplicação possui módulos distintos, cada um oferecendo funcionalidades específicas.

## PRIMEIROS PASSOS [NÃO NECESSARIOS VIA DOCKER]
* ## INSTALE AS DEPENDÊNCIAS NECESSÁRIAS:
    bash
    * poetry install
    * poetry shell

* ### DEFINA AS ENVIROMENTS
    * .env
        * STORE_MERCADO_BITCOIN_BASE_URL=https://store.mercadobitcoin.com.br/api/v1/
        * COTACAO_BASE_URL=https://economia.awesomeapi.com.br/
        * REDIS_HOST=0.0.0.0
        * REDIS_PORT=6379
        * REDIS_TIME=60


## INICIANDO O PROJETO
* FOI CONFIGURADO DUAS OPÇÕES DE DEPURAÇÃOO SENDO ELAS.
    *  EXECUTAR FASTPI -> ONDE IRA SUBIR UMA API PARA FAZER A MANIPULAÇÃO DOS DADOS.

* ### EXECUÇÃO MANUAL.
    * API FASTAPI
        * uvicorn main:app --reload --host 0.0.0.0 --port 8000
## TESTE - MANOEL MESSIAS DA SILVA NETO

Essa aplicação foi construída em Python, utilizando Redis para cache, request e curl-cffi, para requisição. A aplicação possui módulos distintos, cada um oferecendo funcionalidades específicas.

## PRIMEIROS PASSOS [NÃO NECESSÁRIOS VIA DOCKER]
* ## INSTALE AS DEPENDÊNCIAS NECESSÁRIAS:
    ```bash
    poetry install
    poetry shell
    ```

* ### DEFINA AS ENVIRONMENTS
    * .env
        ```env
        STORE_MERCADO_BITCOIN_BASE_URL=https://store.mercadobitcoin.com.br/api/v1/
        COTACAO_BASE_URL=https://economia.awesomeapi.com.br/
        REDIS_HOST=0.0.0.0
        REDIS_PORT=6379
        REDIS_TIME=60
        ```

## INICIANDO O PROJETO
* FOI CONFIGURADO DUAS OPÇÕES DE DEPURAÇÃO SENDO ELAS:
    *  EXECUTAR FASTAPI -> ONDE IRÁ SUBIR UMA API PARA FAZER A MANIPULAÇÃO DOS DADOS.

* ### EXECUÇÃO MANUAL.
    * API FASTAPI
        ```bash
        uvicorn main:app --reload --host 0.0.0.0 --port 8000
        ```

* ### EXECUTAR VIA DOCKER
    * COMANDO
        ```bash
        docker compose up
        ```

## TECNOLOGIAS UTILIZADAS
* **Python 3.12**
    * **Descrição:** 
        Python é uma linguagem de programação de alto nível, conhecida por sua simplicidade e legibilidade. A versão 3.12 inclui várias melhorias de desempenho, novas funcionalidades e aprimoramentos na linguagem.
    * **Para que serve:** 
        É a linguagem de programação principal utilizada para desenvolver a aplicação.

* **FastAPI**
    * **Descrição:**
        FastAPI é um framework web moderno e de alto desempenho para construir APIs com Python 3.6+ baseado em padrões como OpenAPI e JSON Schema. Ele é conhecido por sua facilidade de uso, velocidade e suporte automático à documentação.
    * **Para que serve:**
        É o framework principal utilizado para desenvolver APIs na aplicação, proporcionando uma maneira eficiente e rápida de criar endpoints robustos e bem documentados.

* **Uvicorn**
    * **Descrição:**
        Uvicorn é um servidor ASGI (Asynchronous Server Gateway Interface) rápido e leve, criado para rodar aplicações Python de alto desempenho. Ele é baseado no loop de eventos uvloop e no servidor HTTP httptools, oferecendo suporte total a asyncio, WebSockets e HTTP/2. Uvicorn é conhecido por sua simplicidade, eficiência e compatibilidade com frameworks modernos como FastAPI e Starlette.
    * **Para que serve:**
        Uvicorn é utilizado para servir aplicações web assíncronas, proporcionando baixa latência e alta capacidade de processamento. É ideal para desenvolver APIs rápidas e eficientes, além de suportar recursos modernos como WebSockets e comunicação assíncrona.

* **Requests**
    * **Descrição:**
        Requests é uma biblioteca HTTP para Python, que facilita a realização de requisições HTTP, tratando detalhes complexos das requisições de uma maneira simples e legível.
    * **Para que serve:**
        Utilizada para fazer chamadas HTTP de maneira fácil e eficiente, como consumo de APIs RESTful.

* **Curl-Cffi**
    * **Descrição:**
        Curl-Cffi é uma biblioteca que fornece uma interface de ligação para a biblioteca cURL em Python, permitindo que os desenvolvedores realizem requisições HTTP e manipulem as respostas de forma eficiente. Através de uma API simples, oferece suporte a uma ampla gama de funcionalidades do cURL, incluindo suporte a diferentes protocolos, autenticação e configuração de opções avançadas de conexão.
    * **Para que serve:**
        É utilizada para realizar chamadas HTTP de baixo nível, permitindo um controle detalhado sobre as requisições e respostas, ideal para desenvolvedores que precisam de mais flexibilidade e desempenho em suas interações com APIs e serviços web.

* **Redis**
    * **Descrição:**
        Redis é um armazenamento de estrutura de dados em memória, amplamente utilizado como banco de dados NoSQL, cache e sistema de mensagens. Ele oferece suporte a várias estruturas de dados, como strings, hashes, listas, conjuntos e conjuntos ordenados, e é conhecido por sua alta performance e baixa latência.
    * **Para que serve:**
        É utilizado para melhorar a performance de aplicações ao fornecer acesso rápido a dados frequentemente acessados, implementando caching e sessões de usuário, além de possibilitar a criação de filas de mensagens e pub/sub para comunicação em tempo real entre diferentes componentes de sistemas distribuídos.

* **Pydantic**
    * **Descrição:**
        Pydantic é uma biblioteca de validação de dados para Python, que permite a definição de modelos de dados claros e a validação rigorosa dos dados recebidos e enviados.
    * **Para que serve:**
        Utilizada para garantir a integridade dos dados ao validar e converter dados entre tipos diferentes de maneira automática.

## ESTRUTURA DO PROJETO
```
projeto/
│
├── src/
│   ├── system/
│   │   ├── integrations/
│   │   │   ├── api_coin_gecko.py
│   │   │   ├── api_cotacao.py
│   │   │   └── api_store_mercado_bitcoin.py
│   │   ├── core/
│   │   │   ├── model_core.py
│   │   │   ├── logger_core.py
│   │   │   ├── utils_core.py
│   │   │   ├── redis_core.py
│   │   │   └── database.py
│   │   └── integrations/
│   │   │   ├── api_store_mercado_bitcoin.py
│   │   │   └── api_cotacao.py
│   └── apps/
│       ├── api
│       │   ├── controller.py
│       │   ├── route.py
│       │   └── model.py
│       ├── auth
│       │   ├── controller.py
│       │   ├── route.py
│       │   └── model.py
│       └──
├── .env
├── alembic.ini
├── poetry.lock
├── poetry.toml
└── main.py
```
## AUTOR
#### MANOEL MESSIAS DA SILVA NETO