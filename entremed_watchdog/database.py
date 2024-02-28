from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os

host = (open("/run/secrets/watchdog_db_host", "r").read()).strip()
db = (open("/run/secrets/watchdog_db_name", "r").read()).strip()
user = (open("/run/secrets/watchdog_db_username", "r").read()).strip()
password = (open("/run/secrets/watchdog_db_password", "r").read()).strip()
port = (open("/run/secrets/watchdog_db_port", "r").read()).strip()

SQLALCHEMY_DATABASE_URL = f'postgresql://{user}:{password}@{host}:{port}/{db}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
