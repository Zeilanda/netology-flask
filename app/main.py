from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask('app')
DSN = "postgresql://app:1234@127.0.0.1:5431/netology"

engine = create_engine(DSN)
Session = sessionmaker(bind=engine)