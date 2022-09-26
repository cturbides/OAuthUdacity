import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///menu.db')

"Bind"
DBSession = sessionmaker(bind=engine)
cursor = DBSession()

from restaurant.sql.models import Restaurant, Menu