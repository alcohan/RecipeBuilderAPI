from os import environ
from sqlalchemy import create_engine

server = environ['SERVER']
database = environ['DATABASE']
username = environ['USERNAME']
password = environ['PASSWORD']

DATABASE_URI = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'
engine = create_engine(DATABASE_URI, pool_size=5,max_overflow=2,pool_timeout=30,pool_recycle=3600)
