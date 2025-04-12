"""
Módulo de modelos base do QuentORM
"""
from sqlalchemy import Column as _Column, String as _String, Integer as _Integer, Float as _Float
from sqlalchemy import Boolean as _Boolean, DateTime as _DateTime, ForeignKey as _ForeignKey
from sqlalchemy.orm import relationship as _relationship, DeclarativeBase

class Base(DeclarativeBase):
    """Classe base para todos os modelos do QuentORM"""
    pass

class BaseModel(Base):
    """Classe base para todos os modelos do QuentORM"""
    __abstract__ = True

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={getattr(self, 'id', None)})>"

# Aliases para os tipos do SQLAlchemy
Column = _Column
String = _String
Integer = _Integer
Float = _Float
Boolean = _Boolean
DateTime = _DateTime
ForeignKey = _ForeignKey
relationship = _relationship 