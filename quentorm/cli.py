"""
CLI principal do QuentORM.
Implementa os comandos de linha de comando.
"""

import click
from quentorm import __version__
from .commands import new_command, make_command

@click.group()
def cli():
    """QuentORM CLI - Ferramenta de linha de comando para o QuentORM ORM"""
    pass

cli.add_command(new_command)
cli.add_command(make_command)

if __name__ == '__main__':
    cli() 