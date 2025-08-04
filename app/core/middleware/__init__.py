from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi.middleware import SlowAPIMiddleware
from app.core.configs import Config
from fastapi import FastAPI
from app.core.middleware.SecurityHeadersMiddleware import SecurityHeadersMiddleware
from app.core.middleware.ExceptionHandlerMiddleware import ExceptionHandlerMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.core.middleware.ExceptionHandlerMiddleware import validation_exception_handler

def register_middlewares(app: FastAPI) -> None:
    if Config.APP.ENV == "production":
        app.add_middleware(SlowAPIMiddleware)
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[f"{Config.APP.HOST}:{Config.APP.PORT}", f"http://{Config.APP.HOST}:{Config.APP.PORT}", ],
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allow_headers=["Accept", "Content-Type"],
        )
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=[f"{Config.APP.HOST}:{Config.APP.PORT}", Config.APP.HOST],
        )
        app.middleware("http")(SecurityHeadersMiddleware)

    app.middleware("http")(ExceptionHandlerMiddleware)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    return None