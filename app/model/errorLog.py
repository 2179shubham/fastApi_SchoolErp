# errorLog.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, DateTime
from datetime import datetime

Base = declarative_base()

class ErrorLog(Base):
    __tablename__ = "errorlog"

    id = Column(Integer, primary_key=True, index=True)
    details = Column(Text, nullable=False)  # Using Text to accommodate detailed error messages
    createddate = Column(DateTime, default=datetime.utcnow)