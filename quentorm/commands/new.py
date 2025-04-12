"""
Comando para criar um novo projeto QuentORM
"""

import os
import click
from pathlib import Path
from ..utils.project import (
    create_project_structure,
    create_venv,
    activate_venv,
    install_dependencies,
    create_config_files,
    create_gitignore,
    init_git
)

@click.command('new')
@click.argument('project_name')
def new_command(project_name):
    """Cria um novo projeto QuentORM de forma interativa"""
    click.echo(f"\nCriando novo projeto QuentORM: {project_name}")
    
    # Criar estrutura do projeto
    if click.confirm("Deseja criar a estrutura básica do projeto?", default=True):
        create_project_structure(project_name)
        click.echo("✓ Estrutura do projeto criada com sucesso!")
    
    # Criar ambiente virtual
    if click.confirm("Deseja criar um ambiente virtual?", default=True):
        create_venv(project_name)
        click.echo("✓ Ambiente virtual criado com sucesso!")
        
        # Ativar ambiente virtual
        if click.confirm("Deseja ativar o ambiente virtual?", default=True):
            activate_venv(project_name)
            click.echo("✓ Ambiente virtual ativado!")
            
            # Instalar dependências
            if click.confirm("Deseja instalar as dependências do projeto?", default=True):
                install_dependencies(project_name)
                click.echo("✓ Dependências instaladas com sucesso!")
    
    # Criar arquivos de configuração
    if click.confirm("Deseja criar os arquivos de configuração?", default=True):
        create_config_files(project_name)
        click.echo("✓ Arquivos de configuração criados!")
    
    # Inicializar Git
    if click.confirm("Deseja inicializar um repositório Git?", default=True):
        init_git(project_name)
        create_gitignore(project_name)
        click.echo("✓ Repositório Git inicializado!")
    
    click.echo(f"\nProjeto {project_name} criado com sucesso!")
    click.echo("\nPróximos passos:")
    click.echo("1. cd " + project_name)
    click.echo("2. Ative o ambiente virtual (se ainda não estiver ativo)")
    click.echo("3. Configure o arquivo .env com suas credenciais")
    click.echo("4. Execute 'quentorm migrate' para criar as tabelas") 