from pathlib import Path
from dotenv import load_dotenv
import os
load_dotenv()

class Config:
    class APP:
        HOST = "localhost"
        PORT = 8000
        TITLE = "ACME API by Guigiusti"
        VERSION = "0.0.1"
        CONTACT = {
            "name": "Guigiusti",
            "url": "https://github.com/guigiusti",
        }
        ROOT_PATH = "/api/v1"
        OPENAPI_URL = "/openapi.json"
        DOCS_URL = "/docs"
        REDOC_URL = "/redoc"
        ENV = os.getenv("ENV", "production")

    class DB:
        PATH = Path(__file__).parent / "db.sqlite"
        URL = os.getenv("DB_URL", f"sqlite:///{PATH}")
    class RATE_LIMIT:
        ENABLED = os.getenv("RATE_LIMIT_ENABLED", "false") == "true"
        REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
        RATE = 100
        PER_SECOND = 60


config = Config()