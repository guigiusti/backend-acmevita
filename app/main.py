from contextlib import asynccontextmanager
from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.db import create_tables
from app.api.routes import employee, department, clear_db
from app.core.configs import Config
from app.core.middleware import register_middlewares

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield
limiter = Limiter(key_func=get_remote_address, enabled=Config.RATE_LIMIT.ENABLED, storage_uri=Config.RATE_LIMIT.REDIS_URL, default_limits=[f"{Config.RATE_LIMIT.RATE}/minute"])
app = FastAPI(lifespan=lifespan, 
              root_path=Config.APP.ROOT_PATH,
              openapi_url=Config.APP.OPENAPI_URL,
              docs_url=Config.APP.DOCS_URL,
              redoc_url=Config.APP.REDOC_URL,
              host=Config.APP.HOST, 
              port=Config.APP.PORT,
              version=Config.APP.VERSION,
              title=Config.APP.TITLE,
              contact=Config.APP.CONTACT
              )
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

register_middlewares(app)

app.include_router(employee.router)
app.include_router(department.router)

if Config.APP.ENV == "development": app.include_router(clear_db.router)

@app.get("/")
def home():
    IS_SQLITE = Config.DB.URL.startswith("sqlite")
    DB = "SQLite" if IS_SQLITE else "PostgreSQL"
    return {"message": "ACMEVita API by Guigiusti", "version": Config.APP.VERSION, "DB": DB}

@app.get("/health")
def health():
    return {"status": "ok"}