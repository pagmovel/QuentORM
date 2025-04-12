"""
CLI principal do QuentORM.

Este módulo fornece a interface de linha de comando principal do QuentORM.
"""

import click
from .commands.validator import validator
from .commands.new import new

@click.group()
def cli():
    """Interface de linha de comando do QuentORM."""
    pass

cli.add_command(validator)
cli.add_command(new)

if __name__ == '__main__':
    cli() 