"""
Configurações gerais do sistema.
Define as configurações de ambiente e outras configurações globais.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Configurações gerais do sistema."""
    
    # Configurações de ambiente
    ENV = os.getenv('APP_ENV', 'development')
    DEBUG = os.getenv('APP_DEBUG', 'True').lower() == 'true'
    
    # Configurações de aplicação
    APP_NAME = os.getenv('APP_NAME', 'PyQuent')
    APP_URL = os.getenv('APP_URL', 'http://localhost')
    APP_KEY = os.getenv('APP_KEY', '')
    
    # Configurações de cache
    CACHE_DRIVER = os.getenv('CACHE_DRIVER', 'file')
    CACHE_PREFIX = os.getenv('CACHE_PREFIX', 'pyquent_')
    
    # Configurações de log
    LOG_CHANNEL = os.getenv('LOG_CHANNEL', 'file')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'debug')
    LOG_FILE = os.getenv('LOG_FILE', 'storage/logs/app.log')
    
    @classmethod
    def is_production(cls):
        """Verifica se o ambiente é de produção."""
        return cls.ENV == 'production'
    
    @classmethod
    def is_development(cls):
        """Verifica se o ambiente é de desenvolvimento."""
        return cls.ENV == 'development'
    
    @classmethod
    def is_testing(cls):
        """Verifica se o ambiente é de teste."""
        return cls.ENV == 'testing' 