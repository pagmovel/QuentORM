"""
Módulo de comandos do QuentORM CLI
"""

from .new import new_command
from .migrate import migrate_command
from .seed import seed_command
from .make import make_command

__all__ = [
    'new_command',
    'migrate_command', 
    'seed_command',
    'make_command'
] 