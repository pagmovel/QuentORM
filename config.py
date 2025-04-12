from quentorm import Database
from datetime import timedelta
import os
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

db = Database()

# Configuração de múltiplas conexões
db.config({
    # Conexão principal (MySQL)
    'default': {
        'driver': os.getenv('DB_CONNECTION', 'mysql'),
        'host': os.getenv('DB_HOST', '127.0.0.1'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'database': os.getenv('DB_DATABASE', 'quentorm'),
        'username': os.getenv('DB_USERNAME', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'charset': os.getenv('DB_CHARSET', 'utf8mb4'),
        'collation': os.getenv('DB_COLLATION', 'utf8mb4_unicode_ci'),
        'prefix': os.getenv('DB_PREFIX', ''),
        'strict': os.getenv('DB_STRICT', 'true').lower() == 'true',
        'engine': os.getenv('DB_ENGINE', 'InnoDB'),
        'options': {
            'pool_size': 5,
            'max_overflow': 10,
            'pool_timeout': 30,
            'pool_recycle': 3600,
            'pool_pre_ping': True
        }
    },
    
    # Conexão secundária (PostgreSQL)
    'secondary': {
        'driver': os.getenv('DB_SECONDARY_CONNECTION', 'pgsql'),
        'host': os.getenv('DB_SECONDARY_HOST', '127.0.0.1'),
        'port': int(os.getenv('DB_SECONDARY_PORT', 5432)),
        'database': os.getenv('DB_SECONDARY_DATABASE', 'quentorm_secondary'),
        'username': os.getenv('DB_SECONDARY_USERNAME', 'postgres'),
        'password': os.getenv('DB_SECONDARY_PASSWORD', ''),
        'schema': os.getenv('DB_SECONDARY_SCHEMA', 'public'),
        'options': {
            'pool_size': 5,
            'max_overflow': 10,
            'pool_timeout': 30,
            'pool_recycle': 3600,
            'pool_pre_ping': True
        }
    },
    
    # Conexão terciária (SQLite)
    'tertiary': {
        'driver': os.getenv('DB_TERTIARY_CONNECTION', 'sqlite'),
        'database': os.getenv('DB_TERTIARY_DATABASE', 'quentorm_tertiary.db'),
        'options': {
            'check_same_thread': False
        }
    }
})

# Configuração de cache para cada conexão
db.cache_config({
    'default': {
        'driver': 'redis',
        'host': '127.0.0.1',
        'port': 6379,
        'database': 0,
        'prefix': 'quentorm_',
        'ttl': timedelta(hours=1)
    },
    'secondary': {
        'driver': 'memcached',
        'host': '127.0.0.1',
        'port': 11211,
        'prefix': 'quentorm_secondary_',
        'ttl': timedelta(hours=2)
    }
})

# Configuração de logging para cada conexão
db.logging_config({
    'default': {
        'enabled': True,
        'slow_query_threshold': 1000,
        'log_file': 'logs/queries.log',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    },
    'secondary': {
        'enabled': True,
        'slow_query_threshold': 2000,
        'log_file': 'logs/secondary_queries.log',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    }
}) 