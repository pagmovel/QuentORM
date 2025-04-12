"""
Funções utilitárias para manipulação do projeto
"""

import os
import subprocess
from pathlib import Path

def create_project_structure(project_name):
    """Cria a estrutura básica do projeto"""
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

def create_virtualenv(project_name):
    """Cria um ambiente virtual para o projeto"""
    try:
        subprocess.run(['python', '-m', 'venv', os.path.join(project_name, 'venv')], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def activate_virtualenv(project_name):
    """Ativa o ambiente virtual"""
    if os.name == 'nt':  # Windows
        activate_script = os.path.join(project_name, 'venv', 'Scripts', 'activate')
    else:  # Unix/Linux
        activate_script = os.path.join(project_name, 'venv', 'bin', 'activate')
    
    try:
        os.environ['VIRTUAL_ENV'] = os.path.join(os.getcwd(), project_name, 'venv')
        os.environ['PATH'] = os.path.join(os.environ['VIRTUAL_ENV'], 'bin') + os.pathsep + os.environ['PATH']
        return True
    except Exception:
        return False

def install_dependencies(project_name):
    """Instala as dependências do projeto"""
    try:
        subprocess.run(['pip', 'install', 'quentorm'], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def create_config_files(project_name):
    """Cria os arquivos de configuração do projeto"""
    try:
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
        return True
    except Exception:
        return False

def create_gitignore(project_name):
    """Cria o arquivo .gitignore"""
    try:
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
        return True
    except Exception:
        return False

def init_git(project_name):
    """Inicializa um repositório Git"""
    try:
        subprocess.run(['git', 'init'], cwd=project_name, check=True)
        return True
    except subprocess.CalledProcessError:
        return False 