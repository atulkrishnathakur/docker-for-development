from sqlalchemy import create_engine,MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.loadenv import envconst

SQLALCHEMY_DATABASE_URL = envconst.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

metadata = MetaData()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
