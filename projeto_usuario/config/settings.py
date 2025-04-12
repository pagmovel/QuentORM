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
    APP_NAME = os.getenv('APP_NAME', 'QuentORM')
    APP_URL = os.getenv('APP_URL', 'http://localhost')
    APP_KEY = os.getenv('APP_KEY', '')
    APP_LOCALE = os.getenv('APP_LOCALE', 'pt_br')  # Idioma padrão
    
    # Configurações de cache
    CACHE_DRIVER = os.getenv('CACHE_DRIVER', 'file')
    CACHE_PREFIX = os.getenv('CACHE_PREFIX', 'quentorm_')
    CACHE_TTL = int(os.getenv('CACHE_TTL', '3600'))
    
    # Configurações de log
    LOG_CHANNEL = os.getenv('LOG_CHANNEL', 'file')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'app.log')
    
    # Configurações de segurança
    SECRET_KEY = os.getenv('SECRET_KEY', 'sua_chave_secreta_aqui')
    SESSION_LIFETIME = int(os.getenv('SESSION_LIFETIME', '120'))
    
    # Configurações de banco de dados
    DB_CONNECTION = os.getenv('DB_CONNECTION', 'sqlite')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_DATABASE = os.getenv('DB_DATABASE', 'quentorm')
    DB_USERNAME = os.getenv('DB_USERNAME', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
    
    # Configurações de email
    MAIL_DRIVER = os.getenv('MAIL_DRIVER', 'smtp')
    MAIL_HOST = os.getenv('MAIL_HOST', 'smtp.gmail.com')
    MAIL_PORT = os.getenv('MAIL_PORT', '587')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_ENCRYPTION = os.getenv('MAIL_ENCRYPTION', 'tls')
    MAIL_FROM_ADDRESS = os.getenv('MAIL_FROM_ADDRESS', '')
    MAIL_FROM_NAME = os.getenv('MAIL_FROM_NAME', APP_NAME)
    
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