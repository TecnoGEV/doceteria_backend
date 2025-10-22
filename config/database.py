from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os  # pode trocar para PostgreSQL se quiser

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_engine():
    return engine