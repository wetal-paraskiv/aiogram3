""" Module for postreSQL engine & table creation"""

from os import getenv
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

load_dotenv()

user = getenv("DB_USER")
password = getenv("DB_PASSWORD")
hostname = getenv("DB_HOSTNAME")
port = getenv("DB_PORT")
db_name = getenv("DB_NAME")

url = f"postgresql://{user}:{password}@{hostname}:{port}/{db_name}"
engine = create_engine(url, echo=True)
Base = declarative_base()

