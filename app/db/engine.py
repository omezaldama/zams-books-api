import os

from dotenv import load_dotenv
from sqlmodel import Session, create_engine


load_dotenv(override=True)

connection_string = os.getenv('DB_CONNECTION_STRING')
engine = create_engine(connection_string, echo=False, connect_args={ 'check_same_thread': False })

def get_session():
    with Session(engine) as session:
        yield session
