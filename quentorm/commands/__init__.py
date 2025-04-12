"""
Módulo de comandos do QuentORM CLI
"""

from .new import new_command
from .make import make_command

__all__ = [
    'new_command',
    'make_command'
] 