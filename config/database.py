"""
Configurações do banco de dados.
Define as conexões e parâmetros do banco.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from pyquent import Database

load_dotenv()

class DatabaseConfig:
    """Configurações do banco de dados."""
    
    @staticmethod
    def get_default_connection():
        """Retorna a configuração padrão do banco de dados."""
        return {
            'driver': 'mysql',
            'host': 'localhost',
            'port': 3306,
            'database': 'pyquent',
            'username': 'root',
            'password': '',
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci',
            'prefix': '',
            'strict': True,
            'engine': 'InnoDB',
            'options': {
                'pool_size': 5,
                'max_overflow': 10,
                'pool_timeout': 30,
                'pool_recycle': 3600,
                'pool_pre_ping': True
            }
        }
    
    @staticmethod
    def get_connections():
        """Retorna todas as configurações de conexão."""
        return {
            'default': DatabaseConfig.get_default_connection(),
            'secondary': {
                'driver': 'postgresql',
                'host': 'localhost',
                'port': 5432,
                'database': 'pyquent_secondary',
                'username': 'postgres',
                'password': '',
                'schema': 'public'
            }
        }

class DatabaseManager:
    _instance = None
    _connections = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.config = DatabaseConfig()
        return cls._instance
    
    def connection(self, name=None):
        """Retorna uma conexão com o banco de dados"""
        connection_name = name or 'default'
        
        if connection_name not in self._connections:
            url = self.config.get_connection_url(connection_name)
            engine = create_engine(url)
            Session = sessionmaker(bind=engine)
            self._connections[connection_name] = {
                'engine': engine,
                'session': Session
            }
        
        return self._connections[connection_name]
    
    def get_session(self, name=None):
        """Retorna uma sessão do banco de dados"""
        connection = self.connection(name)
        return connection['session']()
    
    def get_engine(self, name=None):
        """Retorna o engine do banco de dados"""
        connection = self.connection(name)
        return connection['engine']
    
    def get_schema(self, name=None):
        """Retorna o schema do banco de dados"""
        return self.config.get_schema(name)

# Instância global do gerenciador de banco de dados
db = DatabaseManager() 