from .config import Settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

settings = Settings()

# For Testing Purposes
# if settings.db_url == None:
#     with open('config.yaml', 'r') as file:
#         raw_yml = yaml.load(file, Loader=yaml.SafeLoader)
#         db_url = raw_yml["dburl"]

engine = create_engine(settings.db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# # Connect to existing DB
# try:
#     conn = psycopg.connect(host=host , dbname=dbname , user=user, row_factory=dict_row, password=password)  
#     cursor = conn.cursor()
#     print("Database Connection was successful!")
# except Exception as er:
#     print("DB Connection Failure")
#     print("ERROR: ", er)