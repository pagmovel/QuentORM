from quentorm import Base, Model, Column, Integer, String, DateTime, relationship
from datetime import datetime
import json

class User(Base, Model):
    __tablename__ = 'users'
    __fillable__ = ['name', 'email', 'password', 'settings', 'is_admin', 'last_login']
    __hidden__ = ['password']
    __dates__ = ['created_at', 'updated_at', 'last_login']
    __casts__ = {
        'is_admin': 'bool',
        'settings': 'json'
    }
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    settings = Column(String(1000))
    is_admin = Column(Integer, default=0)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relacionamentos
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.original = self.toDict()
    
    def getIsAdminAttribute(self):
        return bool(self.is_admin)
    
    def setIsAdminAttribute(self, value):
        self.is_admin = 1 if value else 0
    
    def getSettingsAttribute(self):
        if not self.settings:
            return {}
        return json.loads(self.settings)
    
    def setSettingsAttribute(self, value):
        self.settings = json.dumps(value)
    
    @classmethod
    def creating(cls, callback):
        cls.__observers__.append(('creating', callback))
    
    @classmethod
    def created(cls, callback):
        cls.__observers__.append(('created', callback))
    
    def __repr__(self):
        return f"<User {self.name}>" 