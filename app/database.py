from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import yaml

with open('config.yaml', 'r') as file:
    raw_yml = yaml.load(file, Loader=yaml.SafeLoader)
    db_url = raw_yml["dburl"]

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
