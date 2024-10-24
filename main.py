from fastapi import  FastAPI, HTTPException,Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.app.api.route import backend as backend_api
from src.app.auth.route import backend as backend_auth

app = FastAPI(
    title="Mercado Bitcoin",
    description="<a href='#' target='__blank'>Teste Manoel Messias da Silva Neto</a>",
    version="0.1.0"
)

# Configurar o CORS
origins = [
    "*",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/",tags=["HOME"])
async def get_home():  
    return {"-- API--"}

app.include_router(backend_api)
app.include_router(backend_auth)


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Manipulador de exceções para erros HTTP específicos.

    Args:
        request (Request): A requisição que causou a exceção.
        exc (StarletteHTTPException): A exceção HTTP levantada.

    Returns:
        JSONResponse: Resposta JSON contendo o código de status, 
                      detalhes da exceção e dados vazios.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status_code": exc.status_code,
            "data": [],
            "detail": exc.detail,
        },
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Manipulador de exceções para erros de validação de requisições.

    Args:
        request (Request): A requisição que causou a exceção.
        exc (RequestValidationError): A exceção de validação levantada.

    Returns:
        JSONResponse: Resposta JSON com código de status 422 e detalhes dos 
                      erros de validação.
    """
    return JSONResponse(
        status_code=422,
        content={
            "status_code": 422,
            "data": [],
            "detail": exc.errors(),
        },
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Manipulador de exceções para erros gerais não tratados.

    Args:
        request (Request): A requisição que causou a exceção.
        exc (Exception): A exceção levantada.

    Returns:
        JSONResponse: Resposta JSON com código de status 500 e detalhes do erro.
    """
    return JSONResponse(
        status_code=500,
        content={
            "status_code": 500,
            "headers": [],
            "detail": str(exc),
        },
    )
