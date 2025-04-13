from quentorm import Model, Column
from sqlalchemy import Integer, String, DateTime, Boolean
from datetime import datetime

class NomeDoModelo(Model):
    __tablename__ = 'nomedomodelos'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
