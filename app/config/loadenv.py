import os
from dotenv import load_dotenv
from typing import Dict
load_dotenv()

class Envconst:
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "atul")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    ALGORITHM =  os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    TOKEN_TYPE: str = "bearer"
    AUTH_HEADER: Dict[str,str] = {"WWW-Authenticate": "Bearer"}
    API_KEY_HEADER_NAME="ACCESS-TOKEN"
    BASE_URL = os.getenv("BASE_URL")

envconst = Envconst()