"""
CLI principal do QuentORM.
Implementa os comandos de linha de comando.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import click
from quentorm import __version__
from .commands import new_command, make_command

def create_project_structure(project_name):
    """Cria a estrutura básica do projeto."""
    dirs = [
        '',
        'app',
        'app/models',
        'app/controllers',
        'app/views',
        'config',
        'database',
        'database/migrations',
        'database/seeders',
        'tests',
    ]
    
    for dir in dirs:
        path = os.path.join(project_name, dir)
        os.makedirs(path, exist_ok=True)
        # Criar __init__.py em cada diretório
        if dir:
            init_file = os.path.join(path, '__init__.py')
            Path(init_file).touch()

def create_config_files(project_name):
    """Cria os arquivos de configuração."""
    # Criar .env.example
    env_example = os.path.join(project_name, '.env.example')
    with open(env_example, 'w') as f:
        f.write("""DB_CONNECTION=sqlite
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=database.sqlite
DB_USERNAME=root
DB_PASSWORD=
""")

    # Criar requirements.txt
    requirements = os.path.join(project_name, 'requirements.txt')
    with open(requirements, 'w') as f:
        f.write("""quentorm>=1.0.0
python-dotenv>=0.19.0
SQLAlchemy>=1.4.0
""")

    # Criar README.md
    readme = os.path.join(project_name, 'README.md')
    with open(readme, 'w') as f:
        f.write(f"""# {project_name}

Projeto criado com QuentORM ORM.

## Instalação

1. Clone o repositório
2. Ative o ambiente virtual:
   ```bash
   source venv/bin/activate  # Linux/Mac
   venv\\Scripts\\activate    # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure o arquivo .env
5. Execute as migrações:
   ```bash
   quentorm migrate
   ```
""")

def create_gitignore(project_name):
    """Cria o arquivo .gitignore."""
    gitignore = os.path.join(project_name, '.gitignore')
    with open(gitignore, 'w') as f:
        f.write("""# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/

# Environment Variables
.env

# IDE
.idea/
.vscode/
*.swp
*.swo

# Database
*.sqlite
*.db
""")

def create_venv(project_name):
    """Cria o ambiente virtual."""
    try:
        subprocess.run([sys.executable, '-m', 'venv', os.path.join(project_name, 'venv')], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def activate_venv(project_name):
    """Ativa o ambiente virtual."""
    if sys.platform == 'win32':
        activate_script = os.path.join(project_name, 'venv', 'Scripts', 'activate')
        subprocess.run(['cmd', '/c', activate_script], shell=True)
    else:
        activate_script = os.path.join(project_name, 'venv', 'bin', 'activate')
        subprocess.run(['source', activate_script], shell=True)

def install_dependencies(project_name):
    """Instala as dependências do projeto."""
    try:
        if sys.platform == 'win32':
            pip = os.path.join(project_name, 'venv', 'Scripts', 'pip')
        else:
            pip = os.path.join(project_name, 'venv', 'bin', 'pip')
        
        subprocess.run([pip, 'install', '-r', os.path.join(project_name, 'requirements.txt')], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def init_git(project_name):
    """Inicializa o repositório Git."""
    try:
        subprocess.run(['git', 'init', project_name], check=True)
        subprocess.run(['git', 'add', '.'], cwd=project_name, check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], cwd=project_name, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

@click.group()
def cli():
    """QuentORM CLI - Ferramenta de linha de comando para o QuentORM ORM"""
    pass

cli.add_command(new_command)
cli.add_command(make_command)

@cli.command()
@click.argument('project_name')
def new(project_name):
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
                if install_dependencies(project_name):
                    click.echo("✓ Dependências instaladas com sucesso!")
                else:
                    click.echo('Erro ao instalar dependências!', err=True)
    
    # Criar arquivos de configuração
    if click.confirm("Deseja criar os arquivos de configuração?", default=True):
        create_config_files(project_name)
        click.echo("✓ Arquivos de configuração criados!")
    
    # Inicializar Git
    if click.confirm("Deseja inicializar um repositório Git?", default=True):
        if init_git(project_name):
            create_gitignore(project_name)
            click.echo("✓ Repositório Git inicializado!")
        else:
            click.echo('Erro ao inicializar Git!', err=True)
    
    click.echo(f"\nProjeto {project_name} criado com sucesso!")
    click.echo("\nPróximos passos:")
    click.echo("1. cd " + project_name)
    click.echo("2. Ative o ambiente virtual (se ainda não estiver ativo)")
    click.echo("3. Configure o arquivo .env com suas credenciais")
    click.echo("4. Execute 'quentorm migrate' para criar as tabelas")

if __name__ == '__main__':
    cli() 